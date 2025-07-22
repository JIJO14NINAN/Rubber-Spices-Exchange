from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import  User_Products

# Create your views here.

def userhome(request):
    template=loader.get_template('Userapp/userhome.html')
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
        return render(request, 'Userapp/user_product_add.html', {'categories': categories, 'subcategories': subcategories})


from Adminapp.models import Login
from .models import User_Products
def user_add_products_view(request):
    user_logins = Login.objects.filter(utype='user')
    users = [login.uid for login in user_logins]
    context = {
        'users': users,
    }
    return render(request, 'Userapp/user_add_products_view.html', context)

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
    return render(request, 'Userapp/user_add_products_view1.html', context)


from Adminapp.models import Admin_Products
def view_products(request):
    products = Admin_Products.objects.all()
    template = loader.get_template("Userapp/view_products.html")
    context = {'products': products}
    return HttpResponse(template.render(context, request))


from datetime import date