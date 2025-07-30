from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from Adminapp.models import Stocks
from Factoryapp.models import Factory
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import FactoryForm
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import logout
import re




# Create your views here.

def factory_home(request):
    template = loader.get_template('FactoryApp/factory_home.html')
    context = {}
    return HttpResponse(template.render(context, request))

   
def factory_register(request):
    if request.method == 'POST':
        form_data = request.POST  # Get the form data from the POST request
        factoryName = form_data.get('facname')  # Use the correct field name
        owner = form_data.get('owner')
        email = form_data.get('email')
        contact = form_data.get('contact')
        license_file = request.FILES.get('license')  # Get the uploaded file
        type = form_data.get('type')
        
        # Perform server-side validation
        errors = {}
        if len(factoryName) < 3 or not re.match(r'^[A-Za-z0-9\s\-]+$', factoryName):
            errors['factoryName'] = "Please enter a valid factory name (min 3 characters, letters/numbers/hyphens)."
        if len(owner) < 3 or not re.match(r'^[A-Za-z\s]+$', owner):
            errors['owner'] = "Please enter a valid owner name (min 3 characters, letters only)."
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors['email'] = "The entered email is invalid. Please enter a valid email address."
        if not re.match(r'^[0-9]{10}$', contact):
            errors['contact'] = "Please enter a valid 10-digit contact number."
        if not license_file:
            errors['license'] = "Please upload a license document."
        if not type:
            errors['type'] = "Please select a factory type."

        if errors:
            return render(request, 'Factory_reg.html', {'success': False, 'errors': errors})
        
        # If valid, save the factory data to the database
        factory = Factory(
            factoryName=factoryName,  # Use the correct field name
            owner=owner,
            email=email,
            contact=contact,
            license=license_file,  # Save the uploaded file
            type=type
        )
        factory.save()  # Save the factory instance to the database

        # Render the success template with a verification message
        return render(request, 'Factory_reg.html', {
            'success': True,
            'message': 'Please wait for the verification.'
        })
    
    # If the request method is not POST, render the registration form
    return render(request, 'Factory_reg.html')

   

def factory_login(request):
    if request.method == 'POST':
        username = request.POST.get('factory_username')
        password = request.POST.get('factory_password')

        # Validation errors
        errors = {}

        # Validate username/email
        if not username:
            errors['username'] = 'Username/Email is required.'
        elif not re.match(r'^[A-Za-z0-9@._-]+$', username):
            errors['username'] = 'Invalid username/email format.'

        # Validate password
        if not password:
            errors['password'] = 'Password is required.'
        elif len(password) < 6:
            errors['password'] = 'Password must be at least 6 characters long.'

        # Return errors if any
        if errors:
            return render(request, 'FactoryApp/factory_login.html', {'success': False, 'errors': errors})

        # Authenticate against the Factory model
        try:
            factory = Factory.objects.get(email=username)  # Assuming email is used for login
            if factory.password == password:  # Replace with hashed password check if applicable
                login(request, factory)  # Log the factory in
                return redirect('factory_home')  # Redirect to the factory home page
            else:
                errors['credentials'] = 'Invalid username/password'
        except Factory.DoesNotExist:
            errors['credentials'] = 'Invalid username/password'

        return render(request, 'FactoryApp/factory_login.html', {'success': False, 'errors': errors})

    return render(request, 'FactoryApp/factory_login.html')  # Render login form for GET requests



   
def factory_stocks(request):
    stocks = Stocks.objects.all()  # Assuming you have a Stocks model to fetch stock data
    return render(request, 'FactoryApp/factory_stocks.html', {'stocks': stocks})   



@login_required
def factory_profile(request):
    """
    View to display and edit factory profile details for the currently logged-in user.
    """
    # Get the factory profile associated with the current user
    factory = get_object_or_404(Factory, owner=request.user.username)  # Assuming owner is the username

    if request.method == 'POST':
        # If the form is submitted, process the data
        form = FactoryForm(request.POST, request.FILES, instance=factory)
        if form.is_valid():
            form.save()  # Save the updated factory details
            return redirect('factory_profile')  # Redirect to the same profile page after saving
    else:
        # If the request is GET, create a form with the current factory data
        form = FactoryForm(instance=factory)

    context = {
        'form': form,
        'factory': factory,
        'page_title': 'Edit Factory Profile',
    }
    
    return render(request, 'FactoryApp/factory_profile.html', context)



def factory_signout(request):
    """
    View to handle factory sign-out (logout) for the currently logged-in user.
    """
    logout(request)
    return redirect('factory_login')