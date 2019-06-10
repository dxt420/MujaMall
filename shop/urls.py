
from django.urls import path
from . import views


app_name = 'shop'


urlpatterns = [
    path('products', views.products , name="products"),
    path('', views.home , name="home"),
    path('products/<slug:c>', views.products , name="products"),
    path('addproduct', views.addproduct , name="addproduct"),
    path('productslist', views.productslist , name="productslist"),
    path('productdetail/<slug:p>', views.productdetail , name="productdetail"),
    path('new', views.new , name="new"),
     path('newcategory', views.newcategory , name="newcategory"),

    

path('addcategory', views.addcategory , name="addcategory"),
# path('get_cart', views.get_cart , name="get_cart"),
# path('add_to_cart/<slug:p>', views.add_to_cart , name="add_to_cart"),

path('cart_add/<slug:product_id>', views.cart_add , name="cart_add"),
path('cart_add2/<slug:product_id>', views.cart_add2 , name="cart_add2"),


path('cart_remove/<slug:product_id>', views.cart_remove , name="cart_remove"),
path('cart_detail', views.cart_detail , name="cart_detail"),

path('postsign', views.postsign , name="postsign"),

path('orders', views.orders , name="orders"),

path('wish', views.wish , name="wish"),

path('account', views.account , name="account"),

path('accountedit', views.accountedit , name="accountedit"),

path('logout', views.logout , name="logout"),

path('login', views.login , name="login"),


path('checkout', views.checkout , name="checkout"),

path('checkoutx', views.checkoutx , name="checkoutx"),

path('checkoutxx', views.checkoutxx , name="checkoutxx"),

path('checkoutxxx', views.checkoutxxx , name="checkoutxxx"),


path('checkout2', views.checkout2 , name="checkout2"),

path('checkout3', views.checkout3 , name="checkout3"),

path('checkout4', views.checkout4 , name="checkout4"),

path('postsignup', views.postsignup , name="postsignup"),


path('signup', views.signup , name="signup"),

path('updatedetail', views.updatedetail , name="updatedetail"),

path('updateship', views.updateship , name="updateship"),

path('viewproducts', views.viewproducts , name="viewproducts"),

path('viewcategories', views.viewcategories , name="viewcategories"),

path('editcategory/<slug:product_id>', views.editcategory , name="editcategory"),
















    

    
]
