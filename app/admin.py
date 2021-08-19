from django.contrib import admin
from .models import Customer,Cart,Product,OrderPlaced
# Register your models here.


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
	list_display=['id','user','name','locality','city','zipcode','state']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
	list_display=['id','title','selling_price','discount_price','description','brand','category','product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
	list_display=['id','user','product','quntity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
	list_display=['id','user','customer','product','quntity','ordered_date','status']