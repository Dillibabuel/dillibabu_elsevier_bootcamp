from django.shortcuts import render

# Create your views here.
def logauth(request):
    return render(request,'logauth/login.html')
def logout(request):
    return render(request,'logauth/logout.html')
def forgotpassword(request):
    return render(request,'logauth/forgotpassword.html')
def register(request):
    return render(request,'logauth/register.html')
def profile(request):
    return render(request,'logauth/profile.html')