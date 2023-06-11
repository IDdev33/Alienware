from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from myapp.serializers import *
from myapp.models import *
from rest_framework.permissions import IsAdminUser, AllowAny
from django.db.models import Sum
from rest_framework.exceptions import ValidationError



class TesView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = [IsAdminUser]
    def get(self,request,*args,**kwargs):
       qs = Product.objects.all()
       serializer = ProductSerializer(qs, many=True)
       return Response(serializer.data)
    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class PublicView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        qs = Product.objects.all()
        serializer = PublicProductSerializer(qs, many=True)
        return Response(serializer.data)    
    
    
class CartAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CartItemSerializer(data=request.data)

        product_id = serializer.initial_data.get('productId')
        action = serializer.initial_data.get('action')

        if not product_id or not action:
            raise ValidationError("Product ID and action are required.")

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError("Product does not exist")

        if request.user.is_authenticated:
            # Handle user case
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        else:
            # Handle guest user case
            guest_identifier = request.COOKIES.get('guest_identifier') 
            try:
                guest_user = GuestUser.objects.get(identifier=guest_identifier)
            except GuestUser.DoesNotExist:
                raise ValidationError("Guest User does not exist")

            customer = guest_user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        
        if action == 'add':
            orderItem.quantity += 1
            print('Item added')
        elif action == 'decrease':
            orderItem.quantity -= 1
            print('Item decreased')
        elif action == 'remove':
            orderItem.delete()
            print('Item removed')
            # Recalculate cart_items after removal
            cart_items = OrderItem.objects.filter(order=order).aggregate(total_items=Sum('quantity'))['total_items']
            
            # Retrieve updated order items and total price after removal
            order_items = OrderItem.objects.filter(order=order)
            order_items_serializer = CartItemSerializer(order_items, many=True)
            cart_total = sum([item.product.price * item.quantity for item in order_items])

            return Response({
                'message': 'Item removed',
                'cartItems': cart_items,
                'orderItems': order_items_serializer.data,
                'cartTotal': cart_total,
            })

        if orderItem.quantity <= 0:
            orderItem.delete()
            return Response({'message': 'Item removed'})

        orderItem.save()

        order_items = OrderItem.objects.filter(order=order)
        order_items_serializer = CartItemSerializer(order_items, many=True)
        cart_items = OrderItem.objects.filter(order=order).aggregate(total_items=Sum('quantity'))['total_items']
        cart_total = sum([item.product.price * item.quantity for item in order_items])

        return Response({
            'message': 'Cart updated successfully',
            'cartItems': cart_items,
            'orderItems': order_items_serializer.data,
            'cartTotal': cart_total,
        })
