// Animation Section
var animatedElements = document.querySelectorAll('.animated');
var isAnimated = [];

animatedElements.forEach(function(animatedElement, index) {
  isAnimated[index] = false;
  animatedElement.setAttribute('data-index', index); // Assign a unique index to the element
});

document.addEventListener('scroll', function() {
  animatedElements.forEach(function(animatedElement) {
    var index = animatedElement.getAttribute('data-index'); // Get the index of the element
    var position = animatedElement.getBoundingClientRect().top;
    var screenPosition = window.innerHeight / 1.3;
    
    if (position < screenPosition && !isAnimated[index]) {
      animatedElement.classList.add('animate__fadeInUp');
      isAnimated[index] = true;
    }
    
    // Check if the element is out of the viewport and remove the animation class to reset it
    if ((position > window.innerHeight || position < -animatedElement.offsetHeight) && isAnimated[index]) {
      animatedElement.classList.remove('animate__fadeInUp');
      isAnimated[index] = false;
    }
  });
});

var isAnimated = [];

animatedElements.forEach(function(animatedElement, index) {
  isAnimated[index] = false;
});

document.addEventListener('scroll', function() {
  animatedElements.forEach(function(animatedElement, index) {
    var position = animatedElement.getBoundingClientRect().top;
    var screenPosition = window.innerHeight / 1.3;
    
    if (position < screenPosition && !isAnimated[index]) {
      animatedElement.classList.add('animate__fadeInUp');
      isAnimated[index] = true;
    }
    
    // Check if the element is out of the viewport and remove the animation class to reset it
    if ((position > window.innerHeight || position < -animatedElement.offsetHeight) && isAnimated[index]) {
      animatedElement.classList.remove('animate__fadeInUp');
      isAnimated[index] = false;
    }
  });
});















// Removal Function

var removeCartItemButtons = document.getElementsByClassName('btn-danger')
for (var i = 0; i < removeCartItemButtons.length; i++) {
    var button = removeCartItemButtons[i]
    button.addEventListener('click', removeCartItem)
}

function removeCartItem(event) {
    var buttonClicked = event.target
    buttonClicked.parentElement.parentElement.remove()
    updateCartTotal()
}


// Calculating Total Function 


function updateCartTotal() {
       var cartItemContainer = document.getElementsByClassName("cart-items")[0]
       var cartRows = cartItemContainer.getElementsByClassName("cart-row")
       var total = 0
       for (var i = 0; i < cartRows.length; i++) {
        var cartRow = cartRows[i]
        var priceElement = cartRow.getElementsByClassName("cart-price")[0]
        var quantityElement = cartRow.getElementsByClassName("cart-quantity-input")[0]
        var price = parseFloat (priceElement.innerText.replace('$', ''))
        var quantity = quantityElement.value
        total = total + (price * quantity)
        console.log(price * quantity)
       }
       document.getElementsByClassName("cart-total-price")[0].innerText = '$' + total
       }
       

// Changing Input Function 


var quantityInputs = document.getElementsByClassName("cart-quantity-input")
for (var i =0; i < quantityInputs.length; i++) {
   var input =  quantityInputs[i]
   input.addEventListener("change", quantityChanged)
}

function quantityChanged(event) {
    var input = event.target
    if (isNaN(input.value) || input.value <= 0){
        input.value = 1

    }
    updateCartTotal()
}

// Add to cart function 
var addToCartbuttons = document.getElementsByClassName("shop-item-button")
for (var i =0; i < addToCartbuttons.length; i++) {
    var button = addToCartbuttons[i]
    button.addEventListener("click", addToCartClicked)
}
async function addToCartClicked(event) {
  var button = event.target;
  var shopItem = button.parentElement.parentElement.parentElement;
  var title = shopItem.getElementsByClassName("shop-item-title")[0].innerText;

  // Fetch product details from the API
  const response = await fetch('http://127.0.0.1:8000/public-products');
  const products = await response.json();
  const product = products.find((p) => p.name === title);

  if (!product) {
      console.error(`Product with name "${title}" not found.`);
      return;
  }

  var price = product.price;
  var imageSrc = product.image;

  // Use the colors field as the image source if no image was provided by the API
  if (!imageSrc && product.colors.length > 0) {
      imageSrc = product.colors[0].image;
  }

  addItemToCart(title, price, imageSrc, shopItem);
  updateCartTotal();
}

function addItemToCart(title, price, imageSrc, shopItem) {
  var cartRow = document.createElement('div');
  cartRow.classList.add('cart-row');
  var cartItems = document.getElementsByClassName('cart-items')[0];
  var cartItemNames = cartItems.getElementsByClassName('cart-item-title');
  for (var i = 0; i < cartItemNames.length; i++) {
    if (cartItemNames[i].innerText == title) {
      alert('This item is already added to the cart');
      return;
    }
  }
  var activeCarousel = shopItem.querySelector('.carousel-item.active');
  if (!activeCarousel) {
    return;
  }
  var imageSrc = activeCarousel.querySelector('.shop-item-image').src;
  var cartRowContents = `
    <div class="cart-item cart-column">
      <img class="cart-item-image" src="${imageSrc}">
      <p class="cart-item-title">${title}</p>
    </div>
    <p class="cart-price cart-column">${price}</p>
    <div class="cart-quantity cart-column">
      <input class="cart-quantity-input" type="number" value="1">
      <button class="btn btn-danger" type="button">DEL</button> 
    </div>`;
  cartRow.innerHTML = cartRowContents;
  cartItems.append(cartRow);
  cartRow.getElementsByClassName('btn-danger')[0].addEventListener('click', removeCartItem);
  cartRow.getElementsByClassName('cart-quantity-input')[0].addEventListener('change', quantityChanged);
}


// If the cart is empty
window.onload = function() {
  const paymentButton = document.getElementById('proceed');
  paymentButton.addEventListener('click', (event) => {
      event.preventDefault();
      const cartItems = document.getElementsByClassName("cart-items")[0];
      const numberOfItemsInCart = cartItems.children.length;
      if (numberOfItemsInCart === 0) {
          alert('There are no items in your cart!');
      } else {
          window.location.href = '/payment';
      }
  });
}



/// Added to cart
let addToCartBtns = document.querySelectorAll(".add-to-cart-button");

let opts = {
  initialText: '<i class="fa fa-cart-arrow-down"></i>Add to Cart',
  textOnClick: '<i class="fa fa-check"></i>Item Added',
  interval: 4000,
};

let setAddToCartText = (addToCartBtn, opt) => {
  addToCartBtn.innerHTML = opt.textOnClick;
  let reinit = () => {
    addToCartBtn.innerHTML = opt.initialText;
  };
  setTimeout(reinit, opt.interval);
};

addToCartBtns.forEach(addToCartBtn => {
  addToCartBtn.addEventListener("click", () => {
    setAddToCartText(addToCartBtn, opts);
  });
});




//Profile Update button
  const first_name = document.querySelector('#first_name');
  const last_name = document.querySelector('#last_name');
  const address = document.querySelector('#address');
  const country = document.querySelector('#country');
  const state = document.querySelector('#state');
  const zip = document.querySelector('#zip');
  const profile_picture = document.querySelector('#profile_picture');
  const update_button = document.querySelector('#update_button');

  // Add an event listener to each input field
  first_name.addEventListener('input', enableUpdateButton);
  last_name.addEventListener('input', enableUpdateButton);
  address.addEventListener('input', enableUpdateButton);
  country.addEventListener('input', enableUpdateButton);
  state.addEventListener('input', enableUpdateButton);
  zip.addEventListener('input', enableUpdateButton);
  profile_picture.addEventListener('input', enableUpdateButton);

  // Define the event listener function
  function enableUpdateButton() {
    // Check if any of the input fields have a non-empty value
    const hasValue = [
      first_name,
      last_name,
      address,
      country,
      state,
      zip,
      profile_picture,
    ].some((input) => input.value.trim() !== '');

    // Enable or disable the update button accordingly
    update_button.disabled = !hasValue;
  }

