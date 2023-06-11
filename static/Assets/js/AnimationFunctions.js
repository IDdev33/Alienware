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


//Back to top button
let mybutton = document.getElementById("btn-back-to-top");
window.onscroll = function () {
  scrollFunction();
};

function scrollFunction() {
  if (
    document.body.scrollTop > 20 ||
    document.documentElement.scrollTop > 20
  ) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}
// When the user clicks on the button, scroll to the top of the document
mybutton.addEventListener("click", backToTop);

function backToTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}