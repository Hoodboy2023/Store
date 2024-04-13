from store import db, login_manager
from store import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserItem(db.Model):
    __tablename__ = 'UserItem' 
    id = db.Column(db.Integer(),primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('User.id'))
    product_id = db.Column(db.String(), db.ForeignKey('Item.id'))
    quantity = db.Column(db.Integer(), nullable=False, default=1)

    user = db.relationship('User', back_populates='items')
    item = db.relationship('Item', back_populates='users')

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    first_name = db.Column(db.String(length=15), nullable=False)
    last_name = db.Column(db.String(length=15), nullable=False)
    phone_number = db.Column(db.String(length=15), nullable=False)
    country = db.Column(db.String(), nullable=False)
    address1 =  db.Column(db.String(length=30), nullable=False)
    address2 = db.Column(db.String(length=30), nullable=False)
    zip = db.Column(db.String(length=15), nullable=False)
    city =  db.Column(db.String(length=20), nullable=False)
    
    items =  db.relationship('UserItem', back_populates='user')

    #budget = db.Column(db.Integer(), nullable=False, default=1000)
    # items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    def __repr__(self):
        return f'<User {self.username}>'

class Item(db.Model):
    __tablename__ = 'Item'
    id = db.Column(db.String(), primary_key=True)
    title = db.Column(db.String(length=30), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    variant_id = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), nullable=False)
    
    users = db.relationship('UserItem', back_populates='item')
    
    def __repr__(self):
        return f'<Item {self.name}>'

        #print(user.id, user.username, user.email_address, user.first_name, user.last_name, user.phone_number, user.country, user.address1, user.address2, user.zip, user.city)