const cartButton =  document.getElementById("cartButton");
const cart = document.getElementById("cart");
let isCartVisible = false;

cartButton.addEventListener("click" ,() => {
  if (isCartVisible === false){
      cart.style.display = "block";
      isCartVisible = true;
  } else {
    cart.style.display = "none";
    isCartVisible = false;
  }
})