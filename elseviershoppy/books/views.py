from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def books(request):
    print('naaz')
    return render(request,'books.html')