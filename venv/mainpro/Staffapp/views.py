from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Staff
from Userapp.models import User_Products
from django.shortcuts import redirect
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.

def staffhome(request):
    template = loader.get_template('Staffapp/staffhome.html')
    context = {}
    return HttpResponse(template.render(context, request))

def assign_task(request, user_id):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        return HttpResponse("<script>alert('assigned successfully!');window.location='/adminhome/';</script>")

# def staff_view_product(request):
#     staff_id = request.session.get('staff_id')
#     if not staff_id:
#         return HttpResponse("Staff not logged in.")

#     staff = Reg.objects.get(id=staff_id)
#     all_products = User_Products.objects.all()
#     product_details = []
#     for product in all_products:
#         user = product.uid
#         product_details.append({
#             'product': product,
#             'user': user,
#         })

#     context = {
#         'product_details': product_details,
#         'staff': staff,
#     }
#     return render(request, "Staffapp/staff_view_product.html", context)

def staff_finished_task(request, product_id):
    try:
        product = User_Products.objects.get(id=product_id)
        product.delete()
        messages.success(request, "Task Finished Successfully")
    except User_Products.DoesNotExist:
        messages.error(request, "Task not found.")
    return redirect('Staffapp/staff_view_product')

# def staff_finished_task(request, product_id):
#     if request.method == "POST":
#         try:
#             product = User_Products.objects.get(id=product_id)
#             product.delete()
#             messages.success(request, "Task Finished Successfully")
#         except User_Products.DoesNotExist:
#             messages.error(request, "Task not found.")
#     return redirect('staff_view_product')