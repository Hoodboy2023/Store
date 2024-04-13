from store import app
from flask import render_template, redirect, url_for, flash, request
from store.models import User,Item, UserItem
from store.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm,EditForm
from store import db
from flask_login import login_user, logout_user, login_required, current_user
from store import bcrypt
from flask import jsonify
from store import PRINTIFY_API_KEY, BASE_URL_PRINTIFY,SHOP_ID
import requests
from store.info import variant_data

@app.route('/')
@app.route('/home')
def home_page():
    #item1 = Item(name="IPhone 15",price=600, barcode="123456789012", description="desc")
    #db.session.add(item1)
    #db.session.commit()
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    if request.method == "POST":
         #p_item_object = Item.query.filter_by(name=purchased_item).first()
        return redirect(url_for('market_page'))

    if request.method == "GET": 
        items =  Item.query.all()
        return render_template('market.html',items=items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password=form.password1.data,
                              first_name=form.first_name.data, last_name=form.last_name.data, country=form.country.data,
                              zip=form.zip_address.data, city=form.city.data, address1=form.address1.data, address2=form.address2.data,
                              phone_number=form.phone_number.data
                              )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/profile', methods=['GET','POST'])
@login_required
def profile_page():
    form = EditForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password=form.password1.data,
                              first_name=form.first_name.data, last_name=form.last_name.data, country=form.country.data,
                              zip=form.zip_address.data, city=form.city.data, address1=form.address1.data, address2=form.address2.data,
                              phone_number=form.phone_number.data
                              )
        db.session.add(user_to_create)
        db.session.commit()
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg[0], category='danger')

    return render_template("user_profile.html",form=form)


@app.route('/profileInfo', methods=['GET'])
@login_required
def profileInfo():
    user_info = {
        "First Name": current_user.first_name,
        "Last Name": current_user.last_name,
        "Username": current_user.username,
        "Email Address": current_user.email_address,
        "Phone Number": current_user.phone_number,
        "Country": current_user.country,
        "Address1": current_user.address1,
        "Address2": current_user.address2,
        "Zip": current_user.zip,
        "City": current_user.city
    }

    return jsonify(user_info)

@app.route("/cart", methods=['POST', 'GET'])
@login_required
def cart():
    data =  request.json
    buttonId = data["buttonId"]
    
    if request.method == 'POST':
        user = User.query.filter_by(id=current_user.id).first()
        item_exists = Item.query.filter_by(id=buttonId).first()
        if item_exists:
            checked_item = None
            for item_to_check in user.items:
                if item_to_check.item.id == buttonId:
                    checked_item = item_to_check
                    break
            if checked_item:
                checked_item.quantity += 1
            else:
                new_item = UserItem(user_id=current_user.id,product_id=buttonId)
                db.session.add(new_item)
            db.session.commit()
            
            response = []
            total_price = 0
            for user_item in user.items: 
                item = user_item.item
                item_total = item.price * user_item.quantity 
                total_price += item_total
                output = {
                    "title": item.title,
                    "image": item.image,
                    "price": item.price,
                    "quantity": user_item.quantity,
                    "item_total": item_total
                }
                response.append(output)
            response.append({"total_price": total_price
                            })
            print(response)
            return jsonify(response)

        
@app.route('/get_products', methods=['GET','POST'])
@login_required
def get_products():
    products = []
    URL = BASE_URL_PRINTIFY + f"shops/{SHOP_ID}/products.json"
    headers = {
        'Authorization': f'Bearer {PRINTIFY_API_KEY}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()  
        products_data = response.json()

        for product in products_data["data"]:
            variants= variant_data[product["id"]]
            item_to_create = Item(id=product["id"],variant_id=variants["variant_id"],title=product['title'],
                                  description=product['description'],price=variants["price"],image=product["images"][0]["src"])
            db.session.add(item_to_create)
            db.session.commit()
        return render_template('api.html',products_data = products_data )
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
   
    
@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))
