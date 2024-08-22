from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def journals(request):
    return render(request,'journals.html')