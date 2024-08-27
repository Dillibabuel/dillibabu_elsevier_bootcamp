from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def books(request):
    return render(request,'books/books.html')