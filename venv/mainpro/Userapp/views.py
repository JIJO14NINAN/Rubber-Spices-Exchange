from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import User_Products, Reg
from Adminapp.models import Cattegory, Subcattegory, Admin_Products
from django.contrib import messages
from django.core.validators import validate_email, ValidationError
from django.contrib.auth.hashers import check_password
from datetime import date
import re
from django.contrib.auth import authenticate, login
from django.contrib import messages


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

        uploadfile = request.FILES.get('uploadfile')

        #Validate required fields
        for field in ['fname', 'sname', 'email', 'phone', 'gender', 'address', 'username', 'password']:
            if not data[field]:
                errors[field] = f"{field.capitalize()} is required."

        if not uploadfile:
            errors['uploadfile'] = "Please upload a document."

        #Email validation
        if 'email' not in errors:
            try:
                validate_email(data['email'])
            except ValidationError:
                errors['email'] = 'Enter a valid email address.'

        #Phone validation (numbers and +)
        if 'phone' not in errors and not re.match(r'^\+?[0-9]{10,15}$', data['phone']):
            errors['phone'] = 'Enter a valid phone number (10-15 digits, numbers and + only).'

        #Location validation
        if not data['location']:
            errors['location'] = 'Location is required.'
        elif data['location'] not in dict(Reg.LOCATION_CHOICES):
            errors['location'] = 'Invalid location selected.'

        #File validation
        if uploadfile:
            if uploadfile.size > 2 * 1024 * 1024:  #2MB limit
                errors['uploadfile'] = "File too large (max 2MB)"
            elif uploadfile.content_type != 'application/pdf':
                errors['uploadfile'] = "Only PDF files are allowed"

        #Username validation (max 16 chars)
        if 'username' not in errors and len(data['username']) > 16:
            errors['username'] = 'Username must be 16 characters or less.'

        #Password validation (complexity)
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

        #Check if username or email already exists
        if 'username' not in errors and Reg.objects.filter(username=data['username']).exists():
            errors['username'] = 'Username already taken.'
        if 'email' not in errors and Reg.objects.filter(email=data['email']).exists():
            errors['email'] = 'Email already registered.'

        if errors:
            return render(request, 'Userapp/Registration.html', {
                'errors': errors,
                'form_data': data,
                'Reg': Reg
            })

        try:
            user = Reg(**data, uploadfile=uploadfile)
            user.save()
            messages.success(request, "Registration successful! Please wait for admin approval.")
            return render(request, 'Userapp/Registration.html', {'Reg': Reg, 'form_data': {}})

        except Exception as e:
            errors['form'] = "An error occurred during registration. Please try again."
            return render(request, 'Userapp/Registration.html', {
                'errors': errors,
                'form_data': data,
                'Reg': Reg
            })

    else:
        return render(request, 'Userapp/Registration.html', {'Reg': Reg})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('user_username')
        password = request.POST.get('user_password')
        try:
            user = Reg.objects.get(username=username)
        except Reg.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return redirect('user_login')
        if not check_password(password, user.password):
            messages.error(request, "Invalid username or password.")
            return redirect('user_login')
        if user.status != 'approved':
            messages.error(request, "Your registration is not authorized by the administrator.")
            return redirect('user_login')
        #Login success: store user id in session
        request.session['user_id'] = user.id
        messages.success(request, f"Welcome, {user.fname}!")
        return redirect('userhome')
    return render(request, 'login.html')

def userhome(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please login first.")
        return redirect('user_login')
    try:
        user = Reg.objects.get(id=user_id)
    except Reg.DoesNotExist:
        messages.error(request, "User not found. Please login again.")
        return redirect('user_login')
    if user.status != 'approved':
        messages.error(request, "Your registration is not authorized by the administrator.")
        return redirect('user_login')
    return render(request, 'Userapp/userhome.html', {'user': user})


def user_add_product(request):
    if request.method == 'POST':
        category_id = request.POST.get('cat')
        subcategory_id = request.POST.get('subcat')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')
        user_id = request.session.get('user_id')

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