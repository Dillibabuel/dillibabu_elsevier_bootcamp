from django.shortcuts import render


# Create your views here.
from django.http import HttpResponse
from .models import ItemDetails

def books(request):
    booklistdata = ItemDetails.objects.all()
    for i in booklistdata:
        print(i.image)
    data = {"bookdata": booklistdata}
    return render(request, 'books/books.html', data)

def booksdetails(request):
    return render (request,'books/booksdetails.html')