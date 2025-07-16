from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import  User_Products

# Create your views here.

def userhome(request):
    template=loader.get_template('userhome.html')
    context={}
    return HttpResponse(template.render(context,request))




from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User_Products
from Adminapp.models import Cattegory, Subcattegory, Reg
from datetime import date

def user_add_product(request):
    if request.method == 'POST':
        category_id = request.POST.get('cat')
        subcategory_id = request.POST.get('subcat')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')
        user_id = request.session.get('uid')

        if not user_id:
            return HttpResponse("<script>alert('User not logged in!');window.location='/login/';</script>")

        if category_id and subcategory_id and quantity and image:
            try:
                category = Cattegory.objects.get(id=category_id)
                subcategory = Subcattegory.objects.get(id=subcategory_id)
                user = Reg.objects.get(id=user_id)

                product = User_Products(
                    uid=user,
                    cid=category,
                    scid=subcategory,
                    qty_in_kg=quantity,
                    img=image,
                    status="pending",
                    date=date.today()
                )
                product.save()
                return HttpResponse("<script>alert('Product added successfully!');window.location='/userhome/';</script>")
            except (Cattegory.DoesNotExist, Subcattegory.DoesNotExist, Reg.DoesNotExist):
                return HttpResponse("<script>alert('Invalid category, subcategory, or user!');window.location='/user_add_product/';</script>")
        else:
            return HttpResponse("<script>alert('All fields are required!');window.location='/user_add_product/';</script>")
    else:
        categories = Cattegory.objects.all()
        subcategories = Subcattegory.objects.all()
        return render(request, 'user_product_add.html', {'categories': categories, 'subcategories': subcategories})


from Adminapp.models import Login
from .models import User_Products
def user_add_products_view(request):
    user_logins = Login.objects.filter(utype='user')
    users = [login.uid for login in user_logins]
    context = {
        'users': users,
    }
    return render(request, 'user_add_products_view.html', context)

def user_add_products_view1(request, user_id):
    user = Reg.objects.get(id=user_id)
    products = User_Products.objects.filter(uid=user)
    staff_logins = Login.objects.filter(utype='staff')
    staffs = [login.uid for login in staff_logins]
    context = {
        'user': user,
        'products': products,
        'staffs': staffs,
    }
    return render(request, 'user_add_products_view1.html', context)
# from Adminapp.models import Login

# def user_add_products_view(request):
#     user_logins = Login.objects.filter(utype='user')
#     users = [login.uid for login in user_logins]
#     context = {
#         'users': users,
#     }
#     return render(request, 'user_add_products_view.html', context)


# def user_add_products_view1(request, user_id):
#     user = Reg.objects.get(id=user_id)
#     products = User_Products.objects.filter(uid=user)
#     staff_logins = Login.objects.filter(utype='staff')
#     staffs = [login.uid for login in staff_logins]
#     context = {
#         'user': user,
#         'products': products,
#         'staffs': staffs,
#     }
#     return render(request, 'user_add_products_view1.html', context)

# def user_add_products_view(request):
#     if request.method == 'POST':
#         category_name = request.POST.get('cat')
#         subcategory_name = request.POST.get('subcat')
#         quantity = request.POST.get('quantity')
#         image = request.FILES.get('image')
#         user_id = request.session.get('uid') 

      
#         if category_name and subcategory_name and quantity and image and user_id:
#             try:
#                 category = Cattegory.objects.get(cname=category_name)
#                 subcategory = Subcattegory.objects.get(scname=subcategory_name)
#                 user = Reg.objects.get(id=user_id)

#                 product = User_Products(
#                     uid=user,
#                     cid=category,
#                     scid=subcategory,
#                     qty_in_kg=quantity,
#                     img=image,
#                     status="pending", 
#                     date=date.today()
#                 )
#                 product.save()
#                 return HttpResponse("<script>alert('Product added successfully!');window.location='/userhome/';</script>")
#             except (Cattegory.DoesNotExist, Subcattegory.DoesNotExist, Reg.DoesNotExist):
#                 return HttpResponse("<script>alert('Invalid category, subcategory, or user!');window.location='/user_add_product/';</script>")
#         else:
#             return HttpResponse("<script>alert('All fields are required!');window.location='/user_add_product/';</script>")
#     else:
#         template=loader.get_template("user_add_products_view.html")
#         context={}
#         return HttpResponse(template.render(context,request))


from Adminapp.models import Admin_Products
def view_products(request):
    products = Admin_Products.objects.all()
    template = loader.get_template("view_products.html")
    context = {'products': products}
    return HttpResponse(template.render(context, request))


def product_details_view(request,id):
    template=loader.get_template("product_details_view.html")
    product = Admin_Products.objects.get(id=id)
    context = {'product': product}
    return HttpResponse(template.render(context, request))


from datetime import date
from .models import Order_Master, Order_Child
from django.db import transaction

def cart_view(request):
    if request.method == 'POST':
        c1 = Cart.objects.all()
        c = Order_Master()
        c.uid = Reg.objects.get(id=request.session['uid'])
        c.order_date = date.today()
        c.gtotal = request.POST['total']  
        c.save()

        for i in c1:
            oc = Order_Child()
            oc.order_id = c
            oc.pid = i.pid
            oc.no_of_items = i.no_of_items
            oc.total = i.total
            oc.status = "pending"
            oc.save()
            subject = "Order Confirmation"
            message = "Your order has been placed successfully. Thank you for shopping with us!"
            from django.conf import settings
            email_from = settings.EMAIL_HOST_USER
            from django.core.mail import send_mail
            subject = "Order Confirmation"  
            mailid = request.POST.get('email')
            recipient_list = [mailid, ]
            send_mail(subject, message, email_from, recipient_list)
        # Clear the cart after placing the order
        for item in c1:
            item.delete()
        return HttpResponse("<script>alert('Order placed successfully!');window.location='/orders_view/';</script>")
    else:
        c = Cart.objects.filter(uid=request.session['uid'])
        total = 0
        for i in c:
            total += i.total
        template = loader.get_template("cart.html")
        context = {'cart': c, 'total': total}
        return HttpResponse(template.render(context, request))        



    
from Adminapp.models import Cart

def add_to_cart(request):
    if request.method == 'POST':
        c = Cart()
        c.uid = Reg.objects.get(id=request.session['uid'])
        c.pid = Admin_Products.objects.get(id=request.POST['pid'])
        c.no_of_items = int(request.POST.get('no_of_items'))
        c.total = int(c.pid.rate) * int(c.no_of_items)
        c.save()
        return HttpResponse("<script>alert('Product added to cart successfully!');window.location='/view_products/';</script>")

      
def cart_remove(request,id):
    cr = Cart.objects.get(id=id)
    cr.delete()
    return HttpResponse("<script>alert('Product removed from cart successfully!');window.location='/cart_view/';</script>")

def cancel_order(request,id):
   cr = Order_Child.objects.get(id=id)
   cr1 = Order_Master.objects.get(id=cr.order_id.id)
   cr.delete()
   return HttpResponse("<script>alert('Order cancelled successfully!');window.location='/view_products/';</script>")

def orders_view(request):
    template=loader.get_template("orders_view.html")
    context={}
    return HttpResponse(("<script>alert('Order placed successfully!');window.location='/view_products/';</script>") + template.render(context,request))


def user_orders(request):
    user_id = request.session.get('uid')
    if not user_id:
        return HttpResponse("<script>alert('User not logged in!');window.location='/login/';</script>")
    orders = Order_Master.objects.filter(uid=user_id)
    order_details = []
    for order in orders:
        order_items = Order_Child.objects.filter(order_id=order.id)
        order_details.append({
            'order': order,
            'items': order_items,
        })

    context = {'order_details': order_details}
    return render(request, 'user_orders.html', context)



def admin_all_user_orders(request):
    orders = Order_Master.objects.all().select_related('uid')
    all_order_details = []
    for order in orders:
        order_items = Order_Child.objects.filter(order_id=order.id).select_related('pid')
        for item in order_items:
            all_order_details.append({
                'user_name': order.uid.name,
                'user_address': order.uid.addr,
                'product_name': item.pid.pname,
                'product_rate': item.pid.rate,
            })
    context = {'all_order_details': all_order_details}
    return render(request, 'admin_all_user_orders.html', context)