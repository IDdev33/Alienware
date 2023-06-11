from django.contrib import admin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'view_products']

    def view_products(self, obj):
        products = obj.get_products()
        product_list = ", ".join([p.name for p in products])
        return product_list

    view_products.short_description = "Products in this category"

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        category_id = request.GET.get('category')
        if category_id:
            return qs.filter(category_id=category_id)
        return qs

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('product_set')
        return qs

    def products(self, obj):
        return ", ".join([p.name for p in obj.product_set.all()])

    products.short_description = 'Products'

admin.site.register(Product, ProductAdmin)
admin.site.register(Profile)
admin.site.register(Image)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)
admin.site.register(ShippingAddress)
admin.site.register(Receipt)
admin.site.register(GuestUser)

