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
import Staffapp.views
import Userapp.views as views
import Adminapp.views as Adminapp_views

urlpatterns = [
    path('staffhome/', Staffapp.views.staffhome, name='staffhome'),
    path('assign_task/<int:user_id>/', Staffapp.views.assign_task, name='assign_task'),
    # path('staff_view_product/', Staffapp.views.staff_view_product, name='staff_view_product'),
    path('staff_finished_task/<int:product_id>/', Staffapp.views.staff_finished_task, name='staff_finished_task'),
    path('logout/', Adminapp_views.logout, name='logout'),
]
