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

import Userapp.views
import Adminapp.views as Adminapp_views

urlpatterns = [
    path('user_add_product/',Userapp.views.user_add_product,name='user_add_product'),
    path('user_add_products_view/',Userapp.views.user_add_products_view,name='user_add_products_view'),
    path('product_details_view/<int:id>/', Userapp.views.product_details_view, name='product_details_view'),
    path('user_add_products_view/', Userapp.views.user_add_products_view, name='user_add_products_view'),
    path('user_add_products_view1/<int:user_id>/', Userapp.views.user_add_products_view1, name='user_products'),
    path('admin_all_user_orders/', Userapp.views.admin_all_user_orders, name='admin_all_user_orders'),
    path('userhome/', Userapp.views.userhome, name='userhome'),
    path('view_products/', Userapp.views.view_products, name='view_products'),
    path('logout/', Adminapp_views.logout, name='logout'),

]

