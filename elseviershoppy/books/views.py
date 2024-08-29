from django.shortcuts import render, get_object_or_404



# Create your views here.
from django.http import HttpResponse
from .models import ItemDetails

def books(request):
    booklistdata = ItemDetails.objects.all().order_by('name')
    data = {"bookdata": booklistdata}
    if(request.method=="POST"):
        category=request.POST.get("category")
        booklistdata = ItemDetails.objects.filter(category=category).all().order_by('name')
        data = {"bookdata": booklistdata}
        print(data)
    
    return render(request, 'books/books.html', data)

def booksdetails(request,id):
    # return render (request,'books/booksdetails.html')
    book = get_object_or_404(ItemDetails, id=id)
    return render(request, 'books/booksdetails.html', {'book': book})