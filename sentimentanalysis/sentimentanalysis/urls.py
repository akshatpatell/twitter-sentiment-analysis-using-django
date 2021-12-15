"""sentimentanalysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth.views import LogoutView


from django.urls import path

from myapp.views import CustomLogin
from myapp.views import show
from myapp.views import prediction
from myapp.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', CustomLogin.as_view(), name='login'),
    path('register',register, name='register'),
    
    path('logout', LogoutView.as_view(next_page = 'login'), name='logout'),
    path('', show, name='show'),
    path('hit', prediction,name = 'prediction'),
]
