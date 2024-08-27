from django.shortcuts import render


# Create your views here.
from django.http import HttpResponse
from .models import ItemDetails

# def books(request):
#     booklistdata = booklist.objects.get(pk=1)
#     data={"bookdata":booklistdata}
#     return render (request,'books/books.html',data)
def books(request):
    booklistdata = ItemDetails.objects.all()
    data = {"bookdata": booklistdata}
    return render(request, 'books/books.html', data)

def booksdetails(request):
    return render (request,'books/booksdetails.html')