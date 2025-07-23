# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import User_Products, Reg
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import User_Products
from Adminapp.models import Cattegory, Subcattegory
from datetime import date
from django.core.validators import validate_email, ValidationError
import re
from datetime import date
from .models import User_Products
from Adminapp.models import Admin_Products


def home(request):
    return render(request, 'index.html')
def user_register(request):
    if request.method == 'POST':
        errors = {}
        
        data = {
            'fname': request.POST.get('fname', '').strip(),
            'sname': request.POST.get('sname', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'phone': request.POST.get('pho', '').strip(),
            'gender': request.POST.get('gender', '').strip(),
            'address': request.POST.get('addr', '').strip(),
            'location': request.POST.get('loc', '').strip(),
            'username': request.POST.get('uname', '').strip(),
            'password': request.POST.get('pswd', '').strip(),
        }

        # Validate required fields
        for field in ['fname', 'sname', 'email', 'phone', 'gender', 'address', 'username', 'password']:
            if not data[field]:
                errors[field] = f"{field.capitalize()} is required."

        # Email validation
        if 'email' not in errors:
            try:
                validate_email(data['email'])
            except ValidationError:
                errors['email'] = 'Enter a valid email address.'

        # Phone validation (numbers and +)
        if 'phone' not in errors and not re.match(r'^\+?[0-9]{10,15}$', data['phone']):
            errors['phone'] = 'Enter a valid phone number (10-15 digits, numbers and + only).'
            
        if not data['location']:
            errors['location'] = 'Location is required.'
        elif data['location'] not in dict(Reg.LOCATION_CHOICES):
            errors['location'] = 'Invalid location selected.'

        # Username validation (max 16 chars)
        if 'username' not in errors and len(data['username']) > 16:
            errors['username'] = 'Username must be 16 characters or less.'

        # Password validation (complexity)
        password = data['password']
        if 'password' not in errors:
            if len(password) < 8:
                errors['password'] = 'Password must be at least 8 characters.'
            elif not re.search(r'[A-Z]', password):
                errors['password'] = 'Password must contain at least 1 uppercase letter.'
            elif not re.search(r'[a-z]', password):
                errors['password'] = 'Password must contain at least 1 lowercase letter.'
            elif not re.search(r'[0-9]', password):
                errors['password'] = 'Password must contain at least 1 number.'
            elif not re.search(r'[^A-Za-z0-9]', password):
                errors['password'] = 'Password must contain at least 1 special character.'

        # Check if username or email already exists
        if 'username' not in errors and Reg.objects.filter(username=data['username']).exists():
            errors['username'] = 'Username already taken.'
        if 'email' not in errors and Reg.objects.filter(email=data['email']).exists():
            errors['email'] = 'Email already registered.'

        if errors:
            return render(request, 'Userapp/Registration.html', {
                'errors': errors,
                'form_data': data,
                'Reg': Reg  # Pass the Reg model to the template
            })

        try:
            user = Reg(**data)
            user.save()
            messages.success(request, "Registration successful! Please wait for admin approval.")
            # Instead of redirect, render the same page with empty form_data and success message
            return render(request, 'Userapp/Registration.html', {
                'Reg': Reg,
                'form_data': {},  # empty form
            })
        except Exception as e:
            errors['form'] = "An error occurred during registration. Please try again."
            return render(request, 'Userapp/Registration.html', {
                'errors': errors,
                'form_data': data,
                'Reg': Reg
            })

    else:
        return render(request, 'Userapp/Registration.html', {'Reg': Reg})  # Pass the Reg model here as well
    
def login(request):
    if request.method == 'POST':
        username = request.POST.get('user_username')
        password = request.POST.get('user_password')
        
        # Basic validation
        if not username or not password:
            return render(request, 'login.html', {'error': 'Username and password are required'})
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('userhome')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')

def userhome(request):
    template=loader.get_template('Userapp/userhome.html')
    context={}
    return HttpResponse(template.render(context,request))

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


def view_products(request):
    products = Admin_Products.objects.all()
    template = loader.get_template("Userapp/view_products.html")
    context = {'products': products}
    return HttpResponse(template.render(context, request))
