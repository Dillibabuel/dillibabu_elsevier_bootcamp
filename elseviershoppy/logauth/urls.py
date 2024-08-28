from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.logauth,name='login'),
    path('register',views.register,name='register'),
    path('logout/', views.logout, name='logout'),
    path('forgotpassword',views.forgotpassword,name='forgotpassword'),
    path('profile',views.profile,name='profile')
    
]
