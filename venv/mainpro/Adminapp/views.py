# views.py

from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Cattegory, Subcattegory, Admin_Products, Stocks
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import CustomAdminLoginForm
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import check_password
from Userapp.models import Reg 
from Staffapp.models import Staff
from django.contrib import messages
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

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
                return redirect('adminhome') 
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

#Decorator to check if user is superuser
def superuser_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser, login_url='admin_login')(view_func))
    return decorated_view_func

@superuser_required
def adminhome(request):
    return render(request, "Adminapp/admin_home.html")

@superuser_required
def view_users_admin(request):
    message = ''
    if request.method == 'POST':
        uid = request.POST.get('uid')
        action = request.POST.get('action')
        try:
            user = Reg.objects.get(id=uid)
            if action == 'activate':
                user.status = 'approved'
                user.save()
                message = f"User {user.username} approved successfully."
            elif action == 'cancel':
                user.delete()
                message = f"User {user.username} rejected and removed."
        except Reg.DoesNotExist:
            message = "User not found."
    #Show only users with status 'pending'
    users = Reg.objects.filter(status='pending').order_by('id')
    return render(request, 'Adminapp/view_users_admin.html', {'users': users, 'message': message})

@superuser_required
def admin_add_staff(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        pho = request.POST.get('pho')
        addr = request.POST.get('addr')
        photo = request.FILES.get('photo')
        uname = request.POST.get('uname')
        pswd = request.POST.get('pswd')

        # Check all fields are filled
        if not all([name, gender, email, pho, addr, photo, uname, pswd]):
            messages.error(request, "Please fill all fields.")
            return render(request, 'Adminapp/admin_add_staff.html', {'form_data': request.POST})

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Enter a valid email address.")
            return render(request, 'Adminapp/admin_add_staff.html', {'form_data': request.POST})

        # Validate phone number (basic: digits only, length 7-15)
        if not re.fullmatch(r'\d{7,15}', pho):
            messages.error(request, "Enter a valid phone number (7-15 digits).")
            return render(request, 'Adminapp/admin_add_staff.html', {'form_data': request.POST})

        # Validate password (basic: min 8 chars, at least one digit and one letter)
        if len(pswd) < 8 or not re.search(r'[A-Za-z]', pswd) or not re.search(r'\d', pswd):
            messages.error(request, "Password must be at least 8 characters long and contain at least one letter and one number.")
            return render(request, 'Adminapp/admin_add_staff.html', {'form_data': request.POST})

        # Check if username already exists
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'Adminapp/admin_add_staff.html', {'form_data': request.POST})

        # Create Django User for staff
        user = User.objects.create_user(username=uname, password=pswd, email=email, first_name=name)
        user.save()

        # Create Staff object
        staff = Staff(
            name=name,
            gender=gender,
            email=email,
            pho=pho,
            addr=addr,
            photo=photo
        )
        staff.save()

        messages.success(request, "Staff added successfully.")
        return redirect('adminhome')

    return render(request, 'Adminapp/admin_add_staff.html')

@superuser_required
def my_staff(request):
    # Retrieve all staff members
    staff_members = Staff.objects.all()
    
    # Calculate total staff and active staff count
    total_staff = staff_members.count()
    active_staff = total_staff  # Assuming all staff are active; adjust logic if needed

    return render(request, 'Adminapp/my_staff.html', {
        'staff_members': staff_members,
        'total_staff': total_staff,
        'active_staff': active_staff,
    })

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
    

def my_stocks(request):
    mystocks = Stocks.objects.all()
    return render(request, 'Adminapp/mystocks.html', {'mystocks': mystocks})