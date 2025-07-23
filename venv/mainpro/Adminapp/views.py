from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from.models import Cattegory,Subcattegory,Admin_Products
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

def index(request):
    template=loader.get_template('Index.html')
    context={}
    return HttpResponse(template.render(context,request))

def adminhome(request):
    template=loader.get_template("Adminapp/adminhome.html")
    context={}
    return HttpResponse(template.render(context,request))
    
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

from django.shortcuts import render, get_object_or_404

def admin_add_product(request):
    if request.method == 'POST':
        cid = request.POST.get('cat')
        pname = request.POST.get('pname')
        desc = request.POST.get('desc')
        img = request.FILES.get('img')  
        rate = request.POST.get('rate')
        qty_in_gm = request.POST.get('qty_in_gm')

        category = get_object_or_404(Cattegory, id=cid)
        product = Admin_Products(
            cid=category,
            pname=pname,
            desc=desc,
            img=img,
            rate=rate,
            qty_in_gm=qty_in_gm
        )
        product.save()
        return HttpResponse("<script>alert('Product added successfully!');window.location='/adminhome/';</script>")
    else:
        categories = Cattegory.objects.all()
        template = loader.get_template("Adminapp/admin_add_product.html")
        context = {'categories': categories}
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
    
from django.shortcuts import redirect

def logout(request):
    request.session.pop('uid', None)
    request.session.pop('staff_id', None)
    # Add other session keys if you use them for admin, e.g. 'admin_id'
    return HttpResponse("<script>alert('Logged out successfully!');window.location='/';</script>")
