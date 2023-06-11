from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import generate_guest_identifier
import json
import random
from django.utils import timezone
from django.http import HttpResponse



# Create your views here.

def cartData(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            # Create a new customer with name and email
            customer = Customer.objects.create(user=request.user, first_name=request.user.first_name, last_name=request.user.last_name, email=request.user.email)
            customer.save()

        try:
            # Retrieve the most recent incomplete order for the customer
            order = Order.objects.filter(customer=customer, complete=False).latest('date_ordered')
        except Order.DoesNotExist:
            # Handle the case when no orders exist
            order = None

        items = []
        if order:
            for item in order.orderitem_set.all():
                images = [image.image.url for image in item.product.image.all()]
                items.append({
                    'id': item.id,
                    'product': {
                        'id': item.product.id,
                        'name': item.product.name,
                        'price': item.product.price,
                        'image_url': images[0] if images else None,
                    },
                    'quantity': item.quantity,
                    'get_total': item.get_total,
                })
        cartItems = order.get_cart_items if order else 0
    else:
        guest_identifier = request.COOKIES.get('guest_identifier')

        if not guest_identifier:
            guest_identifier = generate_guest_identifier()
            response = HttpResponse()
            response.set_cookie('guest_identifier', guest_identifier)  # Set the guest_identifier in the response's cookies

        # Check if a guest user with the guest identifier already exists
        try:
            guest_user = GuestUser.objects.get(identifier=guest_identifier)
        except GuestUser.DoesNotExist:
            guest_user = GuestUser.objects.create(identifier=guest_identifier, first_name='Test', last_name='Test', email='Test@gmail.com')

        # Retrieve or create the associated customer
        customer, created = Customer.objects.get_or_create(guest_user=guest_user)

        if created:
            # Set customer attributes to None if created
            customer.first_name = None
            customer.last_name = None
            customer.email = None
            customer.save()

        # Retrieve the most recent incomplete order for the customer
        order = None  # Set order to None initially
        if customer:
            try:
                order = Order.objects.filter(customer=customer, complete=False).latest('date_ordered')
            except Order.DoesNotExist:
                # Handle the case when no orders exist
                pass

        items = []
        if order:
            for item in order.orderitem_set.all():
                images = [image.image.url for image in item.product.image.all()]
                items.append({
                    'id': item.id,
                    'product': {
                        'id': item.product.id,
                        'name': item.product.name,
                        'price': item.product.price,
                        'image_url': images[0] if images else None,
                    },
                    'quantity': item.quantity,
                    'get_total': item.get_total,
                })

        cartItems = order.get_cart_items if order else 0

    return {'items': items, 'order': order, 'cartItems': cartItems}









# Products
def desktops(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    has_profile_picture = False
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if profile.profile_picture:
                has_profile_picture = True
        except Profile.DoesNotExist:
            pass
    desktop1 = Product.objects.filter(name='Alienware Aurora R15').first()
    desktop2 = Product.objects.filter(name='Alienware Aurora R13').first()
    desktop3 = Product.objects.filter(name='Alienware Aurora Ryzen™ Edition R14').first()
    desktop4 = Product.objects.filter(name='Alienware Aurora R15 Gaming Desktop').first()
    product = Product.objects.all()
    context ={
        'desktop1':  desktop1,
        'desktop2':  desktop2,
        'desktop3':  desktop3,
        'desktop4':  desktop4,
        'has_profile_picture': has_profile_picture,
        'product': product,
        'cartItems': cartItems,
    }
    return render(request, 'desktops.html', context)



def monitors(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    has_profile_picture = False
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if profile.profile_picture:
                has_profile_picture = True
        except Profile.DoesNotExist:
            pass
    monitor1 = Product.objects.filter(name='Alienware 27 Gaming Monitor - AW2723DF').first()
    monitor2 = Product.objects.filter(name='Alienware 34 Curved QD-OLED Gaming Monitor - AW3423DWF').first()
    monitor3 = Product.objects.filter(name='Alienware 34 Curved QD-OLED Gaming Monitor - AW3423DW').first()
    monitor4 = Product.objects.filter(name='Alienware 38 Curved Gaming Monitor | AW3821DW').first()
    product = Product.objects.all()
    context ={
        'monitor1':  monitor1,
        'monitor2':  monitor2,
        'monitor3':  monitor3,
        'monitor4':  monitor4,
        'has_profile_picture': has_profile_picture,
        'product': product,
        'cartItems': cartItems,
    }
    return render(request, 'monitors.html', context)



def laptops(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    has_profile_picture = False
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if profile.profile_picture:
                has_profile_picture = True
        except Profile.DoesNotExist:
            pass
    laptop1 = Product.objects.filter(name='Alienware m17 R5 Gaming Laptop').first()
    laptop2 = Product.objects.filter(name='Alienware x17 R2 Gaming Laptop').first()
    laptop3 = Product.objects.filter(name='Alienware x14 Gaming Laptop').first()
    laptop4 = Product.objects.filter(name='Laptop Dell Alienware Area 51M, 17.3').first()
    product = Product.objects.all()
    context ={
        'laptop1':  laptop1,
        'laptop2':  laptop2,
        'laptop3':  laptop3,
        'laptop4':  laptop4,
        'has_profile_picture': has_profile_picture,
        'product': product,
        'cartItems': cartItems,
    }
    return render(request, 'laptops.html', context)




def keyboards(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    has_profile_picture = False
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if profile.profile_picture:
                has_profile_picture = True
        except Profile.DoesNotExist:
            pass
    keyboard1 = Product.objects.filter(name='Alienware RGB Mechanical Gaming Keyboard - AW410K').first()
    keyboard2 = Product.objects.filter(name='Alienware Low Profile RGB Mechanical Gaming Keyboard - AW510K').first()
    keyboard3 = Product.objects.filter(name='Alienware Tenkeyless Gaming Keyboard').first()
    product = Product.objects.all()
    context ={
        'keyboard1':  keyboard1,
        'keyboard2':  keyboard2,
        'keyboard3':  keyboard3,
        'has_profile_picture': has_profile_picture,
        'product': product,
        'cartItems': cartItems,
    }
    return render(request, 'keyboards.html', context)


def mice(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    has_profile_picture = False
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if profile.profile_picture:
                has_profile_picture = True
        except Profile.DoesNotExist:
            pass
    mouse1 = Product.objects.filter(name='Alienware Wireless Gaming Mouse - AW620M').first()
    mouse2 = Product.objects.filter(name='Alienware Tri-Mode Wireless Gaming Mouse - AW720M').first()
    mouse3 = Product.objects.filter(name='Alienware Wired/Wireless Gaming Mouse | AW610M').first()
    product = Product.objects.all()
    context ={
        'mouse1':  mouse1,
        'mouse2':  mouse2,
        'mouse3':  mouse3,
        'has_profile_picture': has_profile_picture,
        'product': product,
        'cartItems': cartItems,
    }
    return render(request, 'mice.html', context)

def headsets(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    has_profile_picture = False
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if profile.profile_picture:
                has_profile_picture = True
        except Profile.DoesNotExist:
            pass
    headphone1 = Product.objects.filter(name='Alienware Dual Mode Wireless Gaming Headset - AW720H').first()
    headphone2 = Product.objects.filter(name='Alienware Stereo Wired Gaming Headset - AW310H').first()
    headphone3 = Product.objects.filter(name='Alienware AW920H Tri-Mode Wireless Headset').first()
    product = Product.objects.all()
    context ={
        'headphone1':  headphone1,
        'headphone2':  headphone2,
        'headphone3':  headphone3,
        'has_profile_picture': has_profile_picture,
        'product': product,
        'cartItems': cartItems,
    }
    return render(request, 'headsets.html', context)


def chairs(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    has_profile_picture = False
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if profile.profile_picture:
                has_profile_picture = True
        except Profile.DoesNotExist:
            pass
    chair1 = Product.objects.filter(name='Alienware S3800 Comfort Gaming Chair').first()
    chair2 = Product.objects.filter(name='Alienware P4500 Gaming Chair').first()
    chair3 = Product.objects.filter(name='Alienware S5800 Ergonomic Gaming Chair').first()
    chair4 = Product.objects.filter(name='Alienware S5000 Gaming Chair').first()
    product = Product.objects.all()
    context ={
        'chair1':  chair1,
        'chair2':  chair2,
        'chair3':  chair3,
        'chair4':  chair4,
        'has_profile_picture': has_profile_picture,
        'product': product,
        'cartItems': cartItems
    }
    return render(request, 'chairs.html', context)


def bags(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']        
    has_profile_picture = False
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if profile.profile_picture:
                has_profile_picture = True
        except Profile.DoesNotExist:
            pass
    bag1 = Product.objects.filter(name='Wenger Mainframe - Laptop carrying case - 16-inch').first()
    bag2 = Product.objects.filter(name='Dell EcoLoop Pro Sleeve 15-16').first()
    bag3 = Product.objects.filter(name='Dell Gaming Backpack – GM1720PM').first()
    bag4 = Product.objects.filter(name='Alienware Horizon Travel Backpack 18').first()
    product = Product.objects.all()
    context ={
        'bag1':  bag1,
        'bag2':  bag2,
        'bag3':  bag3,
        'bag4':  bag4,
        'has_profile_picture': has_profile_picture,
        'product': product,
        'cartItems': cartItems
    }
    return render(request, 'bags.html', context)


def index(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    has_profile_picture = False
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if profile.profile_picture:
                has_profile_picture = True
        except Profile.DoesNotExist:
            pass

    # Check if the guest identifier cookie is already set
    guest_identifier = request.COOKIES.get('guest_identifier')

    if not guest_identifier:
        # Generate a new guest identifier
        guest_identifier = generate_guest_identifier()

        # Set the guest identifier cookie
        response = render(request, 'index.html', {
            'has_profile_picture': has_profile_picture,
            'cartItems': cartItems,
        })
        response.set_cookie('guest_identifier', guest_identifier)
    else:
        response = render(request, 'index.html', {
            'has_profile_picture': has_profile_picture,
            'cartItems': cartItems,
        })

    return response







# Register Function
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already registered!')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username is taken!')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,
                                                 email=email, password=password)
                user.save();
                return redirect('login')
        else:
            messages.info(request, 'The Passwords Are Not The Same!')
            return redirect('register')   
    else:
        return render(request, 'register.html')
    
    
# Login Function
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login')
    else:
         return render(request, 'login.html')
# Logout Function
def logout(request):
    auth.logout(request)
    return redirect('/')

#Profile function
@login_required
def profile(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        if profile is None:
            profile = Profile(user=user)
        if (user.first_name != request.POST['first_name'] or
            user.last_name != request.POST['last_name']):
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
        if (profile.address != request.POST['address'] or
            profile.city != request.POST['city'] or
            profile.state != request.POST['state'] or
            profile.zipcode != request.POST['zipcode'] or
            'profile_picture' in request.FILES):
            profile.address = request.POST['address']
            profile.city = request.POST['city']
            profile.state = request.POST['state']
            profile.zipcode = request.POST['zipcode']
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            profile.save()

        messages.success(request, 'Your profile has been updated!')
        return redirect('/')
    else:
        context = {
            'profile': profile,
        }
        return render(request, 'profile.html', context)

#Cart

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'cartItems': cartItems, 'items':items,
               'order': order,}
    return render(request, 'cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    user = request.user
    profile_info_retrieved = False
    if user.is_authenticated:
        try:
            profile = user.profile
            profile_info_retrieved = (
                profile.address and profile.city and profile.state and profile.zipcode
            )
        except Profile.DoesNotExist:
            profile = None
    else:
        profile = None
        profile_info_retrieved = False
    context = {'items': items, 'order': order, 'cartItems': cartItems,
               'profile':profile,'profile_info_retrieved': profile_info_retrieved}

    if request.method == 'POST':
        # Process the form data
        info = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'address': request.POST.get('address'),
            'city': request.POST.get('city'),
            'state': request.POST.get('state'),
            'zipcode': request.POST.get('zipcode'),
            'ccn': request.POST.get('ccn'),
            'cardName': request.POST.get('cardName'),
            'expiry_date': request.POST.get('expiry_date'),
            'cvv': request.POST.get('cvv')
        }
        invoice_number = f"INV-{random.randint(100000, 999999)}"
        date_ordered = timezone.now()

        if all(info.values()):
            # Create a new receipt
            if request.user.is_authenticated:
                customer = request.user.customer
                receipt = Receipt.objects.create(order=order, customer=request.user.customer,
                                             invoice_number=invoice_number,
                date_ordered=date_ordered)
                receipt.save()
                ShippingAddress.objects.create(
                        customer=customer,
                        order=order,
                        address=info['address'],
                        city=info['city'],
                        state=info['state'],
                        zipcode=info['zipcode'],
                        )
            else:
              guest_identifier = request.COOKIES.get('guest_identifier')
              guest_user = GuestUser.objects.get(identifier=guest_identifier)
              customer = guest_user.customer
              customer.first_name = info['first_name']
              customer.last_name = info['last_name']
              customer.email = info['email']
              customer.save()
              guest_user.first_name = info['first_name']
              guest_user.last_name = info['last_name']
              guest_user.email = info['email']
              guest_user.save()
              receipt = Receipt.objects.create(order=order, customer=customer,
                invoice_number=invoice_number,date_ordered=date_ordered)
              receipt.save()
              ShippingAddress.objects.create(
                        customer=customer,
                        order=order,
                        address=info['address'],
                        city=info['city'],
                        state=info['state'],
                        zipcode=info['zipcode'],
                        )
            order.complete = True
            transaction_id = f"ID-{random.randint(100000, 999999)}"
            order.transaction_id = transaction_id
            order.save()

            
            # Redirect to the receipt page
            return redirect('receipt', receipt_id=receipt.id)
        else:
            messages.error(request, 'Please fill out all fields')
    return render(request, 'checkout.html', context)

    

    
    
    
    
    
    











# Thank you page function
def receipt(request, receipt_id):
    print('Viewing receipt')
    data = cartData(request)
    cartItems = data['cartItems']

    if request.user.is_authenticated:
        customer = request.user.customer
        first_name = customer.first_name
        last_name = customer.last_name
        customer_email = customer.email
    else:
        try:
            receipt = Receipt.objects.get(id=receipt_id)
            order = receipt.order
            customer = receipt.customer
            first_name = customer.first_name
            last_name = customer.last_name
            customer_email = customer.email
            items = order.orderitem_set.all()
            print('Items for guests:',items)
        except Receipt.DoesNotExist:
            # Handle case where no receipt is found
            messages.error(request, "Receipt not found.")
            return redirect('/')

    try:
        receipt = Receipt.objects.get(id=receipt_id)
        order = receipt.order
        items = order.orderitem_set.all()
        invoice_number = receipt.invoice_number
        current_date = receipt.date_ordered

        context = {
            'items': items,
            'order': order,
            'cartItems': cartItems,
            'invoice_number': invoice_number,
            'date_ordered': current_date,
            'receipt': receipt,
            'first_name': first_name,
            'last_name': last_name,
            'email': customer_email
        }
        return render(request, 'receipt.html', context)
    except Receipt.DoesNotExist:
        # Handle case where no receipt is found
        messages.error(request, "Receipt not found.")
        return redirect('/')
