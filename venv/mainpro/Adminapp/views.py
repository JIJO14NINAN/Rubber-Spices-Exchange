# views.py

from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Cattegory, Subcattegory, Admin_Products
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import CustomAdminLoginForm
from django.contrib.auth import logout as auth_logout
from datetime import datetime
from Adminapp.models import Stocks

def index(request):
    template = loader.get_template('Index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def admin_login(request):
    if request.method == 'POST':
        form = CustomAdminLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active and user.is_superuser:
                login(request, user)
                return redirect('adminhome')  # or your admin dashboard URL name
            else:
                messages.error(request, "You do not have admin access.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAdminLoginForm()
    return render(request, 'Adminapp/admin_login.html', {'form': form, 'app_path': request.path})

def logout(request):
    auth_logout(request)
    return redirect('index')

# Decorator to check if user is superuser
def superuser_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser, login_url='admin_login')(view_func))
    return decorated_view_func

@superuser_required
def adminhome(request):
    return render(request, "Adminapp/admin_home.html")


    
def admin_add_category(request):
    if request.method == 'POST':
        cname = request.POST.get('cat')
        scname = request.POST.get('subcat')
        category, created = Cattegory.objects.get_or_create(cname=cname)
        Subcattegory.objects.create(cid=category, scname=scname)
        return HttpResponse("<script>alert('Category and Subcategory added successfully!');window.location='/adminhome/';</script>")
    else:
        template = loader.get_template("Adminapp/admin_add_category.html")
        context = {}
        return HttpResponse(template.render(context, request))            

def added_products(request):
    products = Admin_Products.objects.all().order_by('-id')  # Latest first
    product_list = []
    for product in products:
        product_list.append({
            'added_date': product.created_at if hasattr(product, 'created_at') else product.id,  # Use created_at if available
            'product_name': product.pname,
            'rate': product.rate,
            'qty': f"{product.qty_in_gm} gm" if product.qty_in_gm else f"{product.qty_in_kg} kg" if hasattr(product, 'qty_in_kg') else "",
        })
    return render(request, 'added_products.html', {'products': product_list})

def view_product(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        action = request.POST.get('action')
        if Admin_Products.objects.filter(id=pid).exists():
            product = Admin_Products.objects.get(id=pid)
            if action == 'delete':
                product.delete()  
                message = f"Product {product.pname} deleted successfully."
            else:
                message = "Invalid action."
        else:
            message = "Product not found."
        products = Admin_Products.objects.all()
        return render(request, 'view_product_admin.html', {'products': products, 'message': message})

    else:
        products = Admin_Products.objects.all()
        return render(request, 'view_products.html', {'products': products})
    


def stocks(request):
    if request.method == 'POST':
        # Get data from the POST request
        date = request.POST.get('date').datetime.now()
        pname = request.POST.get('pname')
        qty_in_kg = request.POST.get('qty_in_kg')
        price = request.POST.get('price')
        status = request.POST.get('status', 'Available')  # Default to 'Available' if not supplied

        # Create a new stock entry
        Stocks.objects.create(pname=pname, qty_in_kg=qty_in_kg, price=price, status=status)

        # Return a success message
        return HttpResponse("<script>alert('Stock added successfully!');window.location='/stocks/';</script>")
    else:
        # Handle GET request to display stocks
        stocks = Stocks.objects.all()
        return render(request, 'Adminapp/mystocks.html', {'stocks': stocks})
    