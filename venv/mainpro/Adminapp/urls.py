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
# urls.py

from django.urls import path
import Adminapp.views

urlpatterns = [
    path('',Adminapp.views.index,name='index'),
    path('admin_login/', Adminapp.views.admin_login, name='admin_login'), 
    path('admin_home/', Adminapp.views.adminhome, name='adminhome'),
    path('admin_add_staff/', Adminapp.views.admin_add_staff, name='admin_add_staff'),
    path('view_users_admin/', Adminapp.views.view_users_admin, name='view_user'),
    path('my_staff/', Adminapp.views.my_staff, name='my_staff'), 
    path('admin_add_category/',Adminapp.views.admin_add_category,name='admin_add_category'),
    path('view_product/',Adminapp.views.view_product,name='view_product'),
    path('my_stocks/', Adminapp.views.my_stocks, name='my_stocks'),
    path('logout/', Adminapp.views.logout, name='logout'),
]
