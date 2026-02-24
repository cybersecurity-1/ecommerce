from django.contrib import admin
from .models import Register
from .models import Product,Cart
from .models import Order,Category,Wishlist,Address

admin.site.register(Register)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Wishlist)
admin.site.register(Address)

# Register your models here.
