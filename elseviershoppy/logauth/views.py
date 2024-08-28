from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
def logauth(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request, 'Username or Password Invalid!')
    return render(request,'logauth/login.html')
def logout(request):
    auth_logout(request)
    return redirect('login')
def forgotpassword(request):
    return render(request,'logauth/forgotpassword.html')
def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username Already Exist')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email Already Exist')
            else:
                user = User.objects.create_user(username=username,password=password,email=email)
                user.save()
                return redirect('profile')

        else:
            messages.error(request, 'Password and Confirm Password Not Matched')
    return render(request,'logauth/register.html')
def profile(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request,'logauth/profile.html', {'user': user})
    else:
        return redirect('index')