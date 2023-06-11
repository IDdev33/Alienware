from rest_framework import serializers
from .models import *
from django.core.exceptions import ObjectDoesNotExist

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'price', 'stock', 'image',)

    def get_image(self, obj):
        if obj.image.exists():
            return obj.image.first().image.url
        else:
            return None
        
class PublicProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'price', 'image',)

    def get_image(self, obj):
        if obj.image.exists():
            return obj.image.first().image.url
        else:
            return None        
    
    
         
class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image.exists():
            return obj.image.first().image.url
        return None

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']


class CartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    action = serializers.ChoiceField(choices=['add', 'decrease', 'remove'])
    product = ProductSerializer(read_only=True)

    def validate(self, attrs):
        product_id = attrs.get('product_id')
        action = attrs.get('action')

        if action == 'add' or action == 'decrease':
            if not product_id:
                raise serializers.ValidationError("Product ID is required.")

            try:
                Product.objects.get(id=product_id)
            except ObjectDoesNotExist:
                raise serializers.ValidationError("Product does not exist.")

        return attrs

    def create(self, validated_data):
        validated_data['product'] = validated_data.pop('product_id')
        return OrderItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data['product'] = validated_data.pop('product_id')
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'quantity', 'action', 'product']
