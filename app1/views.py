from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .models import Register
from .models import Product
from .models import Cart
from .models import Order
from .models import Category
from .models import Wishlist
from .models import Address
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY  # Your test secret key

# Create your views here.
def index(request):
    cat = Category.objects.all().values()
    if 'search' in request.GET:
           search = request.GET['search']
           url = f"/product?search={search}"
           return HttpResponseRedirect(url)
    context = {
        'cat':cat
    }
    

    template = loader.get_template("index.html")
    return HttpResponse(template.render(context,request))

def about(request):
             
    template = loader.get_template("about.html")
    return HttpResponse(template.render({},request))

# def master(request):
#     user = request.session['usersession']
#     wish = Wishlist.objects.filter(wishlist_user = user)
#       # Create a list to store all product IDs
#     pid_list = [x.wishlist_proid for x in wish]  # List comprehension to gather all product IDs

#     context = {
            
#     'pid_lists': pid_list  # Pass the list of product IDs to the context
#     }

#     template = loader.get_template("masterpage.html")
#     return HttpResponse(template.render(context,request))


def account0(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('login')

    user=request.session['usersession'] 
    phonen=Register.objects.filter(reg_username=user).values()
    
    context={

        'phonen':phonen,
      

        }  
    
    
    # if request.method == 'POST':
    #     cname1 = request.POST["name"]
    #     cemail1 = request.POST["email"]
    #     cphone1 = request.POST["phone"]
    #     # cusername1 = request.POST["username"]
    #     # cpsw1 = request.POST["psw"]
    #     cdob1 = request.POST["dob"]
    #     cgender = request.POST["gender"]

    #     reg = Register.objects.filter(reg_username=user)[0]

    #     reg.reg_cname = cname1
    #     reg.reg_cemail = cemail1
    #     reg.reg_cphone = cphone1
    #     # reg.reg_username = cusername1
    #     # reg.reg_psw = cpsw1
    #     reg.reg_date = cdob1
    #     reg.reg_gender = cgender
    #     reg.save()
        # return HttpResponseRedirect('/account?personal')
        # return HttpResponseRedirect('/personal')


    template = loader.get_template("account0.html")
    return HttpResponse(template.render(context,request))

# ...................................................................................................................
# def login(request):
#     if 'usersession' in request.session:
#          return HttpResponseRedirect('/')  
#     if request.method=="POST":
#         log_id = request.POST['log_id']
#         log_psd = request.POST['log_psd']
    
#         login=Register.objects.filter(
#         reg_username=log_id,
#         reg_psw=log_psd
#         )

#         if login:
#             request.session['usersession'] = log_id
#             return HttpResponseRedirect('/')

#     template = loader.get_template("login.html")
#     return HttpResponse(template.render({},request))

def login(request):
    if 'usersession' in request.session:
        return HttpResponseRedirect('/')  

    if request.method == "POST":
        log_id = request.POST['log_id']
        log_psd = request.POST['log_psd']
        
        # Check if the credentials are correct
        login = Register.objects.filter(
            reg_username=log_id,
            reg_psw=log_psd
        )

        if login:
            # Set the user session
            request.session['usersession'] = log_id
            
            # Restore the cart count from the database
            cart_count = Cart.objects.filter(cart_user=log_id).count()
            request.session['cart_count'] = cart_count
            
            # Redirect to the homepage
            return HttpResponseRedirect('/')

    # If not POST, render the login template
    template = loader.get_template("login.html")
    return HttpResponse(template.render({}, request))
# ......................................................................................................................

def register(request):
    if 'usersession' in request.session:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        cname = request.POST["name"]
        cemail = request.POST["email"]
        cphone = request.POST["phone"]
        cusername = request.POST["username"]
        cpsw = request.POST["psw"]
    
        con = Register(
            reg_cname = cname,
            reg_cemail = cemail,
            reg_cphone = cphone,
            reg_username = cusername,
            reg_psw = cpsw,

        )
        con.save()
    template = loader.get_template("register.html")
    return HttpResponse(template.render({},request))

def logout(request):
    if 'usersession' in request.session:
     del request.session['usersession']
    request.session.flush()
    return HttpResponseRedirect('/login')

def addproduct(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    category = Category.objects.all().values()
    if request.method == 'POST':
        pro_name = request.POST['pro_name']
        pro_price = request.POST['pro_price']
        pro_image = request.FILES['pro_image']
        p_catid = request.POST['pro_cats']

        pro_cat = Category.objects.get(id = p_catid)

        product = Product(
            pro_name=pro_name,
            pro_price=pro_price,
            pro_image=pro_image,
            pro_cats=pro_cat,
        )

        product.save()
    context={
        'category':category
    }
    template = loader.get_template("addproduct.html")
    return HttpResponse(template.render(context,request))

def product(request):
      if 'search' in request.GET:
           search = request.GET['search']
           products=Product.objects.filter(pro_name__contains = search)
      elif 'pro' in request.GET:
          id = request.GET['pro']
          products = Product.objects.filter(pro_cats = id)
      else:
        products=Product.objects.all().values()
      user = request.session['usersession']
      if 'del' in request.GET:
          id = request.GET['del']
          delwish = Wishlist.objects.filter(wishlist_proid = id,wishlist_user = user)[0]
          delwish.delete()
          return HttpResponseRedirect("/product")
      wish = Wishlist.objects.filter(wishlist_user = user)
      # Create a list to store all product IDs
      pid_list = [x.wishlist_proid for x in wish]  # List comprehension to gather all product IDs

      context = {
            'products': products,
            'pid_lists': pid_list  # Pass the list of product IDs to the context
        }
      
      template = loader.get_template("product.html")
      return HttpResponse(template.render(context,request))
    
# ..................................................................................................................
# def addtocart(request,id):
#     if 'usersession' not in request.session:
#         return HttpResponseRedirect('/login')

#     exist = Cart.objects.filter(cart_proid=id,cart_user = request.session["usersession"])
#     if exist:
#         exstcart = Cart.objects.filter(cart_proid=id,cart_user = request.session["usersession"])[0]
#         exstcart.cart_qty+=1
#         exstcart.cart_amount = exstcart.cart_qty * exstcart.cart_price
#         exstcart.save()
#     else:
#         pro = Product.objects.filter(id=id)[0]

#         cart = Cart(cart_user = request.session["usersession"],
#                     cart_proid = pro.id,
#                     cart_name = pro.pro_name,
#                     cart_price = pro.pro_price,
#                     cart_image = pro.pro_image,
#                     cart_qty=1,
#                     cart_amount =pro.pro_price)
#         cart.save()
#     return HttpResponseRedirect("/cart")

def addtocart(request, id):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')

    exist = Cart.objects.filter(cart_proid=id, cart_user=request.session["usersession"])
    
    if exist:
        exstcart = exist.first()
        exstcart.cart_qty += 1
        exstcart.cart_amount = exstcart.cart_qty * exstcart.cart_price
        exstcart.save()
    else:
        pro = Product.objects.get(id=id)
        cart = Cart(
            cart_user=request.session["usersession"],
            cart_proid=pro.id,
            cart_name=pro.pro_name,
            cart_price=pro.pro_price,
            cart_image=pro.pro_image,
            cart_qty=1,
            cart_amount=pro.pro_price
        )
        cart.save()

    # Update the cart count in the session
    cart_count = Cart.objects.filter(cart_user=request.session["usersession"]).count()
    request.session['cart_count'] = cart_count
    request.session.modified = True

    return HttpResponseRedirect("/cart")

# .....................................................................................................................
def cart(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    #delete cart item
    if 'del' in request.GET:
        id = request.GET['del']
        delcart = Cart.objects.filter(id=id)[0]
        delcart.delete()

    #change cart quantity
    if 'q' in request.GET:
        q = request.GET['q']
        cp = request.GET['cp']
        cart3= Cart.objects.filter(id=cp)[0]
        if q =='inc':
            cart3.cart_qty+=1
        elif q =='dec':
            if(cart3.cart_qty>1):
                cart3.cart_qty-=1
        cart3.cart_amount = cart3.cart_qty * cart3.cart_price
        cart3.save() 
    user = request.session["usersession"]
    cart=Cart.objects.filter(cart_user=user).values() 
    cart2=Cart.objects.filter(cart_user=user)

    tot = 0
    for x in cart2:
     tot+=x.cart_amount

    shp = tot * 10/100
    # gst = tot *18/100

    # gtot = tot+shp+gst
    gtot = tot+shp
    
    request.session["tot"] = tot
    # request.session["gst"] = gst
    request.session["shp"] = shp
    request.session["gtot"] = gtot

    context={
        'cart':cart,
        'tot':tot,
        'shp':shp,
        # 'gst':gst,
        'gtot':gtot
    }

    templpate = loader.get_template("cart.html")
    return HttpResponse(templpate.render(context,request))

# def checkout(request):
#     if 'usersession' not in request.session:
#         return HttpResponseRedirect('/login')
#     co = 0
#     # adrs = ptype = name = ""
#     adrs = name = lname = pincode = city = state = ""
   

#     #step4 : after order submit
#     if 'div_adrs' in request.POST:
#         adrs = request.POST["div_adrs"]
#         name = request.POST["div_name"]
#         # ptype = request.POST["pay_type"]
#         lname = request.POST["div_lname"]
#         pincode = request.POST["div_zip"]
#         city = request.POST["div_city"]
#         state = request.POST["div_state"]
#         number = request.POST["div_mobile"]
#         user = Register.objects.get(reg_username = request.session["usersession"])
#         address = Address(order_address=adrs, name=name, lname=lname, pincode=pincode, district=city, state=state,mobile = number, username=user)
#         address.save()
#         co=1

#     user = request.session["usersession"]

#     #step1 : delete old data from orders
#     old_odr=Order.objects.filter(order_prouser=user,order_status=0)
#     old_odr.delete()

#     #step2 : add cart data to order table
#     cart=Cart.objects.filter(cart_user=user)
#     for x in cart:
#         odr = Order(order_prouser = x.cart_user,
#                     order_proname = x.cart_name,
#                     order_proprice = x.cart_price,
#                     order_proimage = x.cart_image,
#                     order_proqty = x.cart_qty,
#                     order_proamount = x.cart_amount,
                   
#                     # order_paytype=ptype,
                   
#                     order_status=0
#                       )
#         odr.save()

#     #step3 : Display order data
#     order=Order.objects.filter(order_prouser=user,order_status=0).values()


#     tot = request.session["tot"]
#     # gst = request.session["gst"]
#     shp = request.session["shp"]
#     gtot = request.session["gtot"]

#     phonen=Register.objects.filter(reg_username=user).values()
    
#     context={

#         'order':order,
#         'tot':tot,
#         'shp':shp,
#         # 'gst':gst,
#         'gtot':gtot,
#         'co':co,
#         'phonen':phonen

#         }  
    
         
#     template = loader.get_template("checkout.html")
#     return HttpResponse(template.render(context,request))


def checkout(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    co = 0
    adrs = name = lname = pincode = city = state = ""
    
    if 'div_adrs' in request.POST:
        adrs = request.POST["div_adrs"]
        name = request.POST["div_name"]
        lname = request.POST["div_lname"]
        pincode = request.POST["div_zip"]
        city = request.POST["div_city"]
        state = request.POST["div_state"]
        number = request.POST["div_mobile"]
        user = Register.objects.get(reg_username = request.session["usersession"])
        address = Address(order_address=adrs, name=name, lname=lname, pincode=pincode, district=city, state=state,mobile = number, username=user)
        address.save()
        co=1

    user = request.session["usersession"]

    old_odr=Order.objects.filter(order_prouser=user,order_status=0)
    old_odr.delete()

    cart=Cart.objects.filter(cart_user=user)
    for x in cart:
        odr = Order(order_prouser = x.cart_user,
                    order_proname = x.cart_name,
                    order_proprice = x.cart_price,
                    order_proimage = x.cart_image,
                    order_proqty = x.cart_qty,
                    order_proamount = x.cart_amount,
                    order_status=0
                      )
        odr.save()

    order=Order.objects.filter(order_prouser=user,order_status=0).values()

    tot = request.session["tot"]
    shp = request.session["shp"]
    gtot = request.session["gtot"]

    phonen=Register.objects.filter(reg_username=user).values()
    
    context={

        'order':order,
        'tot':tot,
        'shp':shp,
        'gtot':gtot,
        'co':co,
        'phonen':phonen

        } 
        
    template = loader.get_template("checkout.html")
    return HttpResponse(template.render(context,request))

import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt  # For config if needed

stripe.api_key = settings.STRIPE_SECRET_KEY  # Your test secret key

@csrf_exempt
def stripe_config(request):
    """Return Stripe public key to frontend."""
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)
    return HttpResponse(status=405)

@csrf_exempt
def create_checkout_session(request):
    """Create Stripe Checkout session for payment."""
    if request.method == 'POST':
        # Validate session and cart
        if 'usersession' not in request.session:
            return JsonResponse({'error': 'User not logged in'}, status=401)
        
        total_amount = request.session.get('gtot', 0)
        if not total_amount or total_amount == 0:
            return JsonResponse({'error': 'Invalid or empty cart'}, status=400)
        
        user = request.session.get('usersession')
        domain_url = request.build_absolute_uri('/')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        try:
            # Convert to cents for Stripe
            total_cents = int(float(total_amount) * 100)

            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success/?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Order Total',
                            },
                            'unit_amount': total_cents,
                        },
                        'quantity': 1,
                    }
                ],
                metadata={
                    'user_session': user,
                    'total': str(total_amount),
                }
            )
            print(f"✓ Stripe session created for user {user}: {checkout_session['id']}")
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            print(f"✗ Stripe error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def success(request):
    """Handle successful payment. Fulfill order here."""
    # Optional: Retrieve session via session_id = request.GET.get('session_id')
    # stripe.api_key = settings.STRIPE_SECRET_KEY
    # session = stripe.checkout.Session.retrieve(session_id)

    user = request.session.get('usersession')
    if user:
        # Fulfill: Update orders to paid (status=1), clear cart, etc.
        orders = Order.objects.filter(order_prouser=user, order_status=0)
        orders.update(order_status=1, order_paytype='online')  # Add paytype field if needed
        Cart.objects.filter(cart_user=user).delete()  # Clear cart

        # Redirect to myorders or dashboard
        # return HttpResponseRedirect('/myorders/')

    # Render success template
    context = {'message': 'Payment successful! Your order is confirmed.'}
    template = loader.get_template('success.html')
    return HttpResponse(template.render(context, request))

def cancel(request):
    """Handle cancelled payment."""
    context = {'message': 'Payment cancelled. Feel free to try again.'}
    template = loader.get_template('cancel.html')
    return HttpResponse(template.render(context, request))

# .......................................delevery address......................................




def confirmorder(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    user = request.session["usersession"] 
    order = Order.objects.filter(order_prouser=user,order_status=0) 
    for x in order:
        x.order_status=1
        x.save()
    template = loader.get_template("confirmorder.html")
    return HttpResponse(template.render({},request))  
    
def myorders(request):
    user = request.session["usersession"]
    orders = Order.objects.filter(order_prouser=user, order_status=1)
    
    
    grouped_orders = {}
    for order in orders:
        key = (order.order_proname, order.order_proprice, order.order_proimage)
        if key not in grouped_orders:
            grouped_orders[key] = {
                'order_proname': order.order_proname,
                'order_proprice': order.order_proprice,
                'order_proimage': order.order_proimage,
                'order_proqty': 0,
                'order_proamount': 0
            }
        grouped_orders[key]['order_proqty'] += order.order_proqty
        grouped_orders[key]['order_proamount'] += order.order_proamount
    
   
    order = list(grouped_orders.values())
    
    context = {
        'order': order
    }
    template = loader.get_template("myorders.html")
    return HttpResponse(template.render(context, request))


def profile(request):
    template = loader.get_template("profile.html")
    return HttpResponse(template.render())


# # ........................................................................................................
def delete_from_cart(request, id):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    
    # Find the cart item by product ID and user session
    cart_item = Cart.objects.filter(cart_proid=id, cart_user=request.session['usersession']).first()
    
    if cart_item:
        # Delete the cart item
        cart_item.delete()
        
        # Update the cart count in the session
        cart_count = Cart.objects.filter(cart_user=request.session['usersession']).count()
        request.session['cart_count'] = cart_count
        request.session.modified = True
    
    # Redirect back to the cart page or index page
    return HttpResponseRedirect('/cart')







def add_to_wishlist(request, id):
     if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')

     exist = Wishlist.objects.filter(wishlist_proid=id, wishlist_user=request.session["usersession"])
    
     if exist:
        exstwishlist = exist.first()
        # exstwishlist.cart_qty += 1
        # exstwishlist.cart_amount = exstcart.cart_qty * exstcart.cart_price
        exstwishlist.save()
     else:
        pro = Product.objects.get(id=id)
        wishlist = Wishlist(
            wishlist_user=request.session["usersession"],
            wishlist_proid=pro.id,
            wishlist_name=pro.pro_name,
            wishlist_price=pro.pro_price,
            wishlist_image=pro.pro_image,
            #  cart_qty=1,
            #  cart_amount=pro.pro_price
        )
        wishlist.save()
     return HttpResponseRedirect("/wishlist")
     
def wishlist(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
        
    if 'del' in request.GET:
        id  = request.GET['del']
        delwish = Wishlist.objects.filter(id = id)[0]
        delwish.delete()
    user = request.session["usersession"]
    wish=Wishlist.objects.filter(wishlist_user=user).values() 

    context={

        'wishlist':wish

    } 
    templpate = loader.get_template("wishlist.html")
    return HttpResponse(templpate.render(context,request))



def personal(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('login')
    user=request.session['usersession'] 
    phonen=Register.objects.filter(reg_username=user).values()
    
    context={

        'phonen':phonen,
      

        }  
    
    if request.method == 'POST':
       cname1 = request.POST["name"]
       cemail1 = request.POST["email"]
       cphone1 = request.POST["phone"]
       # cusername1 = request.POST["username"]
       # cpsw1 = request.POST["psw"]
       cdob1 = request.POST["dob"]
       cgender = request.POST["gender"]

       reg = Register.objects.filter(reg_username=user)[0]

       reg.reg_cname = cname1
       reg.reg_cemail = cemail1
       reg.reg_cphone = cphone1
       # reg.reg_username = cusername1
       # reg.reg_psw = cpsw1
       reg.reg_date = cdob1
       reg.reg_gender = cgender
       reg.save()
          
             
    template = loader.get_template("personal.html")
    return HttpResponse(template.render(context,request))

def wallet(request):
             
    template = loader.get_template("wallet.html")
    return HttpResponse(template.render({},request))
def savedaddress(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('login')    
    user=request.session['usersession'] 

    address=Address.objects.filter(username__reg_username=user)

    # add address
    name = add_address = pincode = district = state = ""

    if 'firstName' in request.POST:
        name = request.POST["firstName"]
        add_address = request.POST["address"]
        pincode = request.POST["zipCode"]
        district = request.POST["city"]
        state = request.POST["state"]
        username = Register.objects.get(reg_username=user)

        address = Address(
            name=name,
            order_address=add_address,
            pincode=pincode,
            district=district,
            state=state,
            username=username,
        )
        address.save()
        return HttpResponseRedirect("/savedaddress")

   
    
    
    context = {   
    'address':address,
        
    }


    template = loader.get_template("saved address.html")
    return HttpResponse(template.render(context,request))