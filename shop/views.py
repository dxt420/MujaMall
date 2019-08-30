from django.shortcuts import render,reverse,redirect
from django.http import HttpResponseRedirect
# from cart.cart import Cart
from .cart import Cart
from .forms import CartAddProductForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
# Create your views here.

from pyrebase import pyrebase
from . models import *
from datetime import datetime

from django.conf import settings


import re




from django.dispatch import receiver
from django.http import JsonResponse
import json







config = {
    'apiKey': "AIzaSyA-W5UF_rvGjzUuSxPwNOQb0wO8q0cDl5A",
    'authDomain': "muja-mall.firebaseapp.com",
    'databaseURL':  "https://muja-mall.firebaseio.com",
    'projectId': "muja-mall",
    'storageBucket': "muja-mall.appspot.com",
    'messagingSenderId': "424974719406"


}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()




# email="admin@mujamall.com"
# passw = "admin123"

# auth.sign_in_with_email_and_password(email,passw)
# 

# user = firebase.auth().currentUser

# user = request.session.get('user')



def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get("password")
    try:
        request.session['user'] = auth.sign_in_with_email_and_password(email,passw)
        if request.session.get('checkout_redirect'):
            request.session['checkout_redirect'] = None
            return HttpResponseRedirect(reverse('shop:checkout'))
        else:
            return HttpResponseRedirect(reverse('shop:home'))
    except:
        message = "invalid cerediantials"
        # return render(request,"legalTech\signIn.html",{"msg":message})
        return render(request, "shop/login.html",{"msg":message})
   

def logout(request):
    auth.current_user = None
    request.session['user'] = None
    request.session['checkout_redirect'] =  None
    # auth.logout()
    return HttpResponseRedirect(reverse('shop:home'))




def login(request):
    context = {
        "aaa":"is-active"
    }
    return render(request, 'shop/login.html',context)


def signup(request):
    context = {
        "bbb":"is-active"
    }
    return render(request, 'shop/login.html',context)

def postsignup(request):
    fname=request.POST.get('f_name')
    lname=request.POST.get('l_name')
    name=lname + " " + fname
    email=request.POST.get('email')
    passw=request.POST.get('pass')

    try:
        user=auth.create_user_with_email_and_password(email,passw)
        uid = user['localId']
        data = {
            "first_name":fname,
            "last_name":lname,
            "email":email,
            "uid":uid}
        db.child("users").child(uid).child("details").set(data)
    except:
        message="Unable to create account try again"
        context = {
            "bbb":"is-active",
            "messg":message
        }
        return render(request, 'shop/login.html',context)
        
    context = {
        "aaa":"is-active"
    }
    return render(request, 'shop/login.html',context)







def home(request):
    # if request.session.get('user'):
    #     categories = db.child("categories").get()
    #     context = {
    #         "categories":categories,
    #         "aa":"is-active",
    #     }
    #     # num = request.session.get('num')
    #     print(request.session.get('user'))
    #     return render(request,"shop/home.html",context)
    # else:
    #     print(request.session.get('user'))
    #     return render(request, "shop/login.html")
    cart = Cart(request)
    uuu = None
    if request.session.get('user'):
        uuu = db.child("users").child(request.session.get('user')['localId']).child("details").get()

    categories = db.child("categories").get()
    context = {
        "categories":categories,
        "aa":"is-active",
        'cart': cart,
        "user":uuu
    }
    return render(request,"shop/home.html",context)

    
    
def productslist(request):
    return render(request,"shop/product-list.html")

def products(request,c):
    # products = db.child("products").orderBy("category").startAt(c).endAt(c).get()
    uuu = None
    if request.session.get('user'):
        uuu = db.child("users").child(request.session.get('user')['localId']).child("details").get()
    
    pro = db.child("products").get()
    cat = db.child("categories").child(c).get()
    
    for p in pro.each():
    
        pk = p.key()
        products = []
        pp = None
        if p.val()['category'] == cat.val()['name']:
            pp = p.val()
            pp['key'] = p.key()

            products.append(pp)


    cc = Cart(request)
    item = None
    for item in cc:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    context = {
        "products":products,
        "aa":"is-active",
        "cat":cat,
        "cart": cc,
        "item":item,
        "user":uuu
    }

 
    return render(request,"shop/products.html",context)

def productdetail(request,p):
    product = db.child("products").child(p).get()
    cart_product_form = CartAddProductForm()
    cart = Cart(request)
    uuu = db.child("users").child(request.session.get('user')['localId']).child("details").get()

    context = {
        "product":product,
        "aa":"is-active",
        'cart_product_form': cart_product_form,
        'cart': cart,
        "user":uuu
    }
    return render(request,"shop/product-detail.html",context)

def new(request):
    categories = db.child("categories").get()
    context = {
        "categories":categories
    }
    return render(request,"shop/admin/new.html",context)

def viewproducts(request):
    products = db.child("products").get()
    context = {
        "products":products
    }
    return render(request,"shop/admin/products.html",context)

def viewcategories(request):
    products = db.child("products").get()
    categories = db.child("categories").get()
    context = {
        "categories":categories,
        "products":products
    }
    return render(request,"shop/admin/categories.html",context)

def newcategory(request):
    return render(request,"shop/admin/new2.html")






def orders(request):
    uuu = db.child("users").child(request.session.get('user')['localId']).child("details").get()
    context = {
        "cc":"is-active",
        "user":uuu
    }
    return render(request,"shop/orders.html",context)

def wish(request):
    uuu = db.child("users").child(request.session.get('user')['localId']).child("details").get()
    context = {
        "dd":"is-active",
        "user":uuu
    }
    return render(request,"shop/wish.html",context)

def account(request):
    u = db.child("users").child(request.session.get('user')['localId']).child("details").get()
   
    ship = db.child("users").child(request.session.get('user')['localId']).child("shipping_details").get()
   
    context = {
        "ee":"is-active",
        "user":u,
        "ship":ship
    }
    return render(request,"shop/account.html",context)
    
def addproduct(request):
    
    
    now = datetime.today().strftime("%Y%m%d%H%M%S")
    
    storage = firebase.storage()
    # as user
    user = request.session.get('user')
    thename = request.FILES['pic']
    new_product_pic = Product(icon=request.FILES['pic'])      
    new_product_pic.save()
    print(new_product_pic.icon.url)
    s = new_product_pic.icon.url + " "
    s = re.sub('/.*?/', '', s)
    # print(s)
    filer = re.sub('media', '', settings.MEDIA_ROOT)
    storage.child("products/"+s).put(filer + new_product_pic.icon.url, user['idToken'])
    url = storage.child("products/"+s).get_url(user['idToken'])
    data = {
        "name": request.POST.get('name'),
        "model": request.POST.get('model'),
        "description": request.POST.get('description'),
        "category": request.POST.get('category'),
        "price": request.POST.get('price'),
        "imageurl": url
    }

    results = db.child("products").push(data, user['idToken'])
    
    return HttpResponseRedirect(reverse('shop:home'))
    # rproductseturn render(request,"shop/product-detail.html")

def addcategory(request):
    data = {
        "name": request.POST.get('name')
    }

    results = db.child("categories").push(data, user['idToken'])
    
    return HttpResponseRedirect(reverse('shop:home'))
    # return render(request,"shop/product-detail.html")

def editcategory(request,product_id):
    old_name = request.POST.get('previous_name')
    aaa = db.child("products").get()
    
    aa = None

    for a in aaa.each():
        aa = db.child("products").order_by_child("category").equal_to(old_name).get()
        
    data = {
        "name": request.POST.get('name'),
        "featured": request.POST.get('featured'+product_id)
    }

    data2 = {
        "category": request.POST.get('name')
    }
    db.child("categories").child(product_id).update(data)


    

   
    
    for b in aa.each():
        print(b.val())
        db.child("products").child(b.key()).update(data2)
    print("done")
    return JsonResponse({"hello":"hello"}, safe=False)
    

    # return JsonResponse(abc, safe=False)
    # return render(request,"shop/admin/new2.html")
























# def add_to_cart(request, p):
#     product = db.child("products").child(p).get()
#     cart = Cart(request)
#     quantity = request.GET.get('qty')
#     print(quantity)
#     # cart.add(product, product.val()['price'], quantity)

# # def remove_from_cart(request, product_id):
# #     product = Product.objects.get(id=product_id)
# #     cart = Cart(request)
# #     cart.remove(product)

# def get_cart(request):
#     return render(request, 'cart.html', {'cart': Cart(request)})











@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    # product = get_object_or_404(Product, id=product_id)
    pro = db.child("products").child(product_id).get()
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data

        # product = []
        # product.append(pro.val())
        # print(product)
        cart.add(product=pro, quantity=cd['quantity'], update_quantity=cd['update'])
    else:
        print("bitch am invalid")
    
    # with cart.__len__ as total_items:
    abc = {
        "total_items":cart.__len__()
    }
   
    return JsonResponse(abc, safe=False)
  
    # return HttpResponseRedirect(reverse('shop:productdetail', kwargs={'p': pro.key()}))

 



def cart_add2(request, product_id):
    cart = Cart(request)
    # product = get_object_or_404(Product, id=product_id)
    pro = db.child("products").child(product_id).get()
    cart.add(product=pro, quantity=1, update_quantity=False)
    categories = db.child("categories").get()
    cat_key = None
    for cc in categories.each():
        if cc.val()['name'] == pro.val()['category']:
            cat_key = cc.key()
    

    return HttpResponseRedirect(reverse('shop:products', kwargs={'c': cat_key}))


def cart_remove(request, product_id):
    cart = Cart(request)
    pro = db.child("products").child(product_id).get()
    cart.remove(pro)
    
    return HttpResponseRedirect(reverse('shop:cart_detail'))

def cart_remove2(request, product_id):
    cart = Cart(request)
    pro = db.child("products").child(product_id).get()
    cart.remove(pro)
    
    categories = db.child("categories").get()
    cat_key = None
    for cc in categories.each():
        if cc.val()['name'] == pro.val()['category']:
            cat_key = cc.key()
    

    return HttpResponseRedirect(reverse('shop:products', kwargs={'c': cat_key}))


def cart_detail(request):
    if request.session.get('user'): 
        u = db.child("users").child(request.session.get('user')['localId']).child("details").get()
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
        return render(request, 'shop/cart.html', {'cart': cart,   "bb":"is-active","user":u})
    else:
        return render(request, 'shop/cart.html', {"bb":"is-active"})
    



def checkout(request):
    request.session['checkout_redirect'] =  "oblivion"
    if request.session.get('user'): 
        print(request.session.get('user')['localId'])
        u = db.child("users").child(request.session.get('user')['localId']).child("details").get()
        context = {
            "user":u
        }
        return render(request, 'shop/checkout-step-1.html',context)
        # return render(request, 'shop/checkout-step-1.html')
    else:
        return render(request, "shop/login.html")

def checkout2(request):
    u = db.child("users").child(request.session.get('user')['localId']).child("details").get()
    ship = db.child("users").child(request.session.get('user')['localId']).child("shipping_details").get()
   
    context = {
        "ship":ship,
        "user":u
    }
    
    return render(request, 'shop/checkout-step-2.html',context)

def checkout3(request):
    u = db.child("users").child(request.session.get('user')['localId']).child("details").get()
    cart = Cart(request)
    context = {
        "cart":cart,
        "user":u
    }
    return render(request, 'shop/checkout-step-3.html',context)

def checkout4(request):
    u = db.child("users").child(request.session.get('user')['localId']).child("details").get()
    return render(request, 'shop/checkout-step-4.html')
    # return render(request, 'shop/checkout-step-5.html')
    

def checkoutx(request):
    checkout_data_1 = {
        "fname": request.POST.get('fname'),
        "lname": request.POST.get('lname'),
        "email": request.POST.get('email')
    }
    request.session['checkout_data_1'] =  checkout_data_1
    return HttpResponseRedirect(reverse('shop:checkout2'))

def checkoutxx(request):
    checkout_data_2 = {
        "address": request.POST.get('address'),
        "state": request.POST.get('state'),
        "zip": request.POST.get('zip'),
        "country": request.POST.get('country'),
        "city": request.POST.get('city'),
        "street": request.POST.get('street')
    }
    request.session['checkout_data_2'] =  checkout_data_2
    return HttpResponseRedirect(reverse('shop:checkout3'))


def checkoutxxx(request):
    checkout_data_3 = {
        "address": request.POST.get('address'),
        "state": request.POST.get('state'),
        "zip": request.POST.get('zip'),
        "country": request.POST.get('country'),
        "city": request.POST.get('city'),
        "street": request.POST.get('street')
    }
    request.session['checkout_data_3'] =  checkout_data_3
    return HttpResponseRedirect(reverse('shop:checkout4'))





def updatedetail(request):

    data = {
            "first_name":request.POST.get('fname'),
            "last_name":request.POST.get('lname'),
            "email":request.POST.get('email'),
            "phone":request.POST.get('phone')
    }
    db.child("users").child(request.session.get('user')['localId']).child("details").update(data)
    return HttpResponseRedirect(reverse('shop:accountedit'))


def updateship(request):

    data = {
            "address":request.POST.get('address'),
            "city":request.POST.get('city'),
            "state":request.POST.get('state'),
            "street":request.POST.get('street'),
            "zip":request.POST.get('zip'),
            "country":request.POST.get('country')
    }
    db.child("users").child(request.session.get('user')['localId']).child("shipping_details").set(data)
    return HttpResponseRedirect(reverse('shop:accountedit'))


def accountedit(request):


    u = db.child("users").child(request.session.get('user')['localId']).child("details").get()

    ship = db.child("users").child(request.session.get('user')['localId']).child("shipping_details").get()
   
    context = {
        "ee":"is-active",
        "user":u,
        "ship":ship
    }

    return render(request, "shop/account-edit.html",context)

    