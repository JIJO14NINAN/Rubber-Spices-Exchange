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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Userapp.views.home, name='index'),
    path('reg/', Userapp.views.user_register, name='reg'),
    path('login/', Userapp.views.user_login, name='user_login'),
    # path('logout/', Userapp.views.user_logout, name='user_logout'),
    path('userhome/', Userapp.views.userhome, name='userhome'),
    path('view_products/', Userapp.views.view_products, name='view_products'),   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
