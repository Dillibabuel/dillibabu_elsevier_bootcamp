from django.shortcuts import render
from checkout.models import OrderDetails, OrderItemMapping
from django.db.models import Sum


 
# Create your views here.
from django.http import HttpResponse
 
def home(request):
    user_id = request.user.id
    order = OrderDetails.objects.filter(userid=user_id, status='In Progress').first()

    total_quantity = 0
    if order:
        total_quantity = OrderItemMapping.objects.filter(orderDetails=order).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0
    return render (request,'index.html',{'total_quantity':total_quantity})
 
