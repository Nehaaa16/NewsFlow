"""
URL configuration for NewsProj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path("register/",views.register_user,name="registeruser"),
    path("login/",views.login_user,name="login"),
    path("logout/",views.logout_user,name="logout"),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('createprofile/', views.createProfile, name='createprofile'),
    path('editprofile/<str:username>/', views.editProfile, name='editprofile'),
    path("payment/",views.makePayment,name="payment"),
    path("premium/",views.premiumPlans,name="premium"),
    path("savepost/",views.savepost,name="savepost"),


]
