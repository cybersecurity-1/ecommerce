from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('about',views.about,name='about'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('account0',views.account0,name='account0'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('product',views.product,name='product'),
    path('addtocart/<int:id>',views.addtocart,name='addtocart'),
    path('cart',views.cart,name='cart'),
    path('checkout',views.checkout,name='checkout'),
    path('confirmorder',views.confirmorder,name='confirmorder'),
    path('myorders',views.myorders,name='myorders'),
    path('cart/delete/<int:id>/', views.delete_from_cart, name='delete_from_cart'),
    path('add_to_wishlist/<int:id>',views.add_to_wishlist,name='add_to_wishlist'),
    path('wishlist',views.wishlist,name='wishlist'),
    path('personal',views.personal,name='personal'),
    path('wallet',views.wallet,name='wallet'),
    path('savedaddress',views.savedaddress,name='savedaddress'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)