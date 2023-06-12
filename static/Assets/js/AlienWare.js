function updateUserOrder(productId, action) {
  console.log('Sending data...');
  var url = '/api/cart/';

  // Determine the request body based on the user's authentication status
  var requestBody = {};
  if (user === 'AnonymousUser') {
    requestBody = {
      'productId': productId,
      'action': action,
    };
  } else {
    requestBody = {
      'productId': productId,
      'action': action,
      'guestUser': false,
    };
  }

  // Make AJAX request to the API endpoint
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify(requestBody),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Failed to update cart. Please try again.');
      }
      return response.json();
    })
    .then((data) => {
      console.log('data:', data);
      var cartTotalElement = document.getElementById('cart-total');
      cartTotalElement.textContent = parseInt(data.cartItems);

      // Update the cart items and total price on the cart page
      updateCartUI(data);
      
      // Update the total price in the footer
      var totalElement = document.querySelector('.shopping-cart-footer .total');
      var totalPriceFormatted = data.cartTotal ? data.cartTotal.toFixed(2) : '';


      totalElement.textContent = 'Total: $' + totalPriceFormatted;
    })
    .catch((error) => {
      console.error('Error:', error);
      console.log('Response:', error.response);
      // Display error message to the user
    });
}


// Function to update the cart items and total price on the cart page
function updateCartUI(data) {
  var cartItemsContainer = document.querySelector('.shopping-cart tbody');

  // Clear the container before populating with new items
  cartItemsContainer.innerHTML = '';

  data.orderItems.forEach((item) => {
    var cartItemElement = document.createElement('tr');
    if (item.product) {
      var itemPrice = item.product.price * item.quantity;
      var totalPriceFormatted = itemPrice ? itemPrice.toFixed(2) : '';

      cartItemElement.innerHTML = `
        <td>
          <div class="product-item">
            <img class="product-thumb" src="${item.product.image}" alt="${item.product.name}">
            <div class="product-info">
              <span>${item.product.name}</span>
            </div>
          </div>
        </td>
        <td class="text-center">
          <p data-product="${item.product.id}" data-action="add" class="update-cart arrows"><i class="fa fa-arrow-up" style="color: #5bc0de;"></i></p>
          <p>${item.quantity}</p>
          <p data-product="${item.product.id}" data-action="decrease" class="update-cart arrows"><i class="fa fa-arrow-down" style="color: #5bc0de;"></i></p>
        </td>
        <td class="text-center text-lg text-medium">&nbsp;$${item.product.price}</td>
        <td class="text-center text-lg text-medium">$${totalPriceFormatted}</td>
        <td class="text-center"><button data-product="${item.product.id}" data-action="remove" class="btn btn-danger update-cart remove-from-cart">Del</button></td>
      `;
    } else {
      cartItemElement.innerHTML = '<td colspan="5">Item not found</td>';
    }
    cartItemsContainer.appendChild(cartItemElement);
  });

  var totalElement = document.querySelector('.shopping-cart-footer .total');
  var totalPriceFormatted = data.cartTotal ? data.cartTotal.toFixed(2) : '';
  totalElement.textContent = 'Total: $' + totalPriceFormatted;

  // Handle remove button click event
  var removeButtons = document.querySelectorAll('.remove-from-cart');
  removeButtons.forEach((button) => {
    button.addEventListener('click', function() {
      var productId = this.dataset.product;
      var action = this.dataset.action;

      // Send AJAX request to the server to remove the item
      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/api/cart/', true);
      xhr.setRequestHeader('Content-type', 'application/json');
      xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
          // Item removed successfully
          var response = JSON.parse(xhr.responseText);
          updateCartUI(response); // Update the cart UI with the updated data
        }
      };
      var data = JSON.stringify({ productId: productId, action: action });
      xhr.send(data);
    });
  });
}


// Cart Functions:
var updateBtns = document.getElementsByClassName('add-btn');
for (var i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener('click', function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log('productId:', productId, 'action:', action);
    updateUserOrder(productId, action);
    console.log('USER', user);

    // Update the button text
    var opts = {
      initialText: '<i class="fa fa-cart-arrow-down"></i>Add to Cart',
      textOnClick: '<i class="fa fa-check"></i>Item Added',
      interval: 3000,
    };

    setButtonText(this, opts);
  });
}

function setButtonText(button, options) {
  var initialText = button.innerHTML;
  button.innerHTML = options.textOnClick;
  setTimeout(function () {
    button.innerHTML = initialText;
  }, options.interval);
}


// Cart Functions:
var cartItemsContainer = document.querySelector('.shopping-cart tbody');
cartItemsContainer.addEventListener('click', function (event) {
  var updateBtn = event.target.closest('.update-cart');
  if (updateBtn) {
    var productId = updateBtn.dataset.product;
    var action = updateBtn.dataset.action;
    console.log('productId:', productId, 'action:', action);
    updateUserOrder(productId, action);
    console.log('USER', user);
  }
});


















