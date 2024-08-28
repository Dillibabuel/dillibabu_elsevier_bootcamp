from django.shortcuts import render, get_object_or_404



# Create your views here.
from django.http import HttpResponse
from .models import ItemDetails

def books(request):
    booklistdata = ItemDetails.objects.all()
    data = {"bookdata": booklistdata}
    return render(request, 'books/books.html', data)

def booksdetails(request,id):
    # return render (request,'books/booksdetails.html')
    book = get_object_or_404(ItemDetails, id=id)
    return render(request, 'books/booksdetails.html', {'book': book})