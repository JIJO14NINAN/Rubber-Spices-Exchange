"""
URL configuration for mainpro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path


import Adminapp.views




urlpatterns = [
    
    path('',Adminapp.views.index,name='index'),
    path('reg/',Adminapp.views.reg,name='reg'),
    path('login/',Adminapp.views.login,name='login'),
    path('adminhome/', Adminapp.views.adminhome, name='adminhome'),
    path('view_user/',Adminapp.views.view_user,name='view_user'),
    path('admin_add_category/',Adminapp.views.admin_add_category,name='admin_add_category'),
    path('admin_add_product/',Adminapp.views.admin_add_product,name='admin_add_product'),
    path('view_product/',Adminapp.views.view_product,name='view_product'),
    path('admin_add_staff/',Adminapp.views.admin_add_staff,name='admin_add_staff'),
    path('orders_details_view/',Adminapp.views.orders_details_view,name='orders_details_view'),
    path('logout/', Adminapp.views.logout, name='logout'),
   

]
