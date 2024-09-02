from django.shortcuts import render, get_object_or_404
from checkout.models import OrderDetails, OrderItemMapping
from django.db.models import Sum




# Create your views here.
from django.http import HttpResponse
from .models import ItemDetails

def books(request):
    user_id = request.user.id
    order = OrderDetails.objects.filter(userid=user_id, status='In Progress').first()
    

    total_quantity = 0
    if order:
        total_quantity = OrderItemMapping.objects.filter(orderDetails=order).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0
        totalitem = 0
    if order:
        totalitem = OrderItemMapping.objects.filter(orderDetails=order).count()

    booklistdata = ItemDetails.objects.all().order_by('name')
    data = {"bookdata": booklistdata,"total_quantity":total_quantity}

    if request.method == "POST":
        category = request.POST.get("category")
        if category == "all":
            booklistdata = ItemDetails.objects.all().order_by('name')
        else:
            booklistdata = ItemDetails.objects.filter(category=category).order_by('name')
        data = {"bookdata": booklistdata,"total_quantity":total_quantity}

    return render(request, 'books/books.html', data)


def booksdetails(request,id):
    user_id = request.user.id
    order = OrderDetails.objects.filter(userid=user_id, status='In Progress').first()
    

    total_quantity = 0
    if order:
        total_quantity = OrderItemMapping.objects.filter(orderDetails=order).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0
    book = get_object_or_404(ItemDetails, id=id)
    print(book)
    return render(request, 'books/booksdetails.html', {'book': book,'total_quantity': total_quantity})