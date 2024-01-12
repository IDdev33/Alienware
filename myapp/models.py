from django.db import models
from django.contrib.auth.models import User
from .utils import generate_guest_identifier


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name 
    def get_products(self):
        return Product.objects.filter(category=self)      
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    reviews_score = models.FloatField()
    reviews_url = models.URLField(blank=True, default='')
    spec1 = models.CharField(max_length=200, blank=True)
    spec2 = models.CharField(max_length=200, blank=True)
    spec4 = models.CharField(max_length=200, blank=True)
    spec3 = models.CharField(max_length=200, blank=True)
    spec5 = models.CharField(max_length=200, blank=True)
    spec6 = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='', null=True)
    image = models.ManyToManyField('Image', blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.name
    
class Image(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/')
    def __str__(self):
        return self.name
   
    @property
    def imageURL(self):
        try:
          url = self.image.url
        except:
          url = ''
        return url
 


class GuestUser(models.Model):
    identifier = models.CharField(max_length=20, default=generate_guest_identifier, unique=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return f"Guest User {self.identifier}"
 
 
 
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    guest_user = models.OneToOneField(GuestUser, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    def save(self, *args, **kwargs):
        if self.user:
            self.email = self.user.email
        super().save(*args, **kwargs)
    
    
    
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)  
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True) 


    def __str__(self):
        return str(self.id)
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def shipping(self):
        orderitems = self.orderitem_set.all()
        shipping = False
        for i in orderitems:
            if i.product.requires_shipping():
                shipping = True
                break 
        return shipping   

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True)    
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100) 
    def __str__(self):
        return self.product.name
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
     
    
class Receipt(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100)
    date_ordered = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'Receipt {self.id} for {self.customer.last_name}'
    
        

class ShippingAddress(models.Model):
      customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True, null=True)
      order = models.ForeignKey(Order,on_delete=models.SET_NULL, null=True)
      address = models.CharField(max_length=200, null=False)
      state = models.CharField(max_length=200, null=False)
      city = models.CharField(max_length=200, null=False)
      zipcode = models.CharField(max_length=200, null=False)
      date_added = models.DateTimeField(auto_now_add=True) 

      def __str__(self):
          return self.address









        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  
    def __str__(self):
        return self.user.username
    def has_info(self):
        return self.user and self.address and self.city and self.state and self.zipcode 
