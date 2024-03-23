from django import urls
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib import admin


from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
     #####################################################
    path('signup/driver/', views.DriverSignupView.as_view()),
    path('signup/', views.CustomerSignupView.as_view()),
    path('login/',views.CustomAuthToken.as_view(), name='auth-token'),
    path('logout/', views.LogoutView.as_view(), name='logout-view'),
    ##############################################
] 