const cartButton =  document.getElementById("cartButton");
const cart = document.getElementById("cart");
const profileDisplay = document.getElementById("profile_display");
const editDisplay = document.getElementById("edit_display");
const displayToggle1 = document.getElementById("displaytoggle1");
const displayToggle2 = document.getElementById("sumbit2");
const firstnameinput = document.getElementById("first_name");
const lastnameinput = document.getElementById("last_name");
const usernameinput = document.getElementById("username");
const emailaddressinput = document.getElementById("email_address");
const phonenumberinput = document.getElementById("phone_number");
const countryinput = document.getElementById("country");
const address1input = document.getElementById("address1");
const address2input = document.getElementById("address2");
const zipinput = document.getElementById("zip_address");
const cityinput = document.getElementById("city");
let isCartVisible = false;
let isEditDisplayVisible = false;


const profileInfo = async () => {
   try {
     const results = await fetch('/profileInfo');
     const data = await results.json();
     countryinput.value = data["Country"];
     usernameinput.value = data["Username"];
     firstnameinput.value = data["First Name"];
     lastnameinput.value = data["Last Name"];
     emailaddressinput.value = data["Email Address"];
     phonenumberinput.value = data["Phone Number"];
     address1input.value = data["Address1"];
     address2input.value = data["Address2"];
     zipinput.value = data["Zip"];
     cityinput.value = data["City"]


   } catch (err){
    console.error(err)
   }
  }

  profileInfo()



displayToggle1.addEventListener("click", () => {
  if (isEditDisplayVisible === false){
    editDisplay.style.display = 'block';
    profileDisplay.style.display = 'none';
    isEditDisplayVisible = true;
  }

  displayToggle2.addEventListener("click", () => {
    if (isEditDisplayVisible === false){
      editDisplay.style.display = "none";
      profileDisplay.style.display = "block";
      isEditDisplayVisible = false;
    }
  })
})
cartButton.addEventListener("click" ,() => {
  if (isCartVisible === false){
      cart.style.display = "block";
      isCartVisible = true;
  } else {
    cart.style.display = "none";
    isCartVisible = false;
  }
})