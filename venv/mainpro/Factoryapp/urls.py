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
import Factoryapp.views

urlpatterns = [
    path('factory_login/', Factoryapp.views.factory_login, name='factory_login'),
    path('factory_register/', Factoryapp.views.factory_register, name='factory_register'),
    path('factory_home/', Factoryapp.views.factory_home, name='factory_home'), 
    path('factory_profile/', Factoryapp.views.factory_profile, name='factory_profile'),
    path('factory_stocks/', Factoryapp.views.factory_stocks, name='factory_stocks'),
]