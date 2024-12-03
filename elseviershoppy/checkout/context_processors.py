from .models import OrderDetails, OrderItemMapping
from django.db.models import Sum

def cart_item_count(request):
    totalitem = 0
    total_quantity = 0
    
    if request.user.is_authenticated:
        user_id = request.user.id
        order = OrderDetails.objects.filter(userid=user_id, status='In Progress').first()
        if order:
            totalitem = OrderItemMapping.objects.filter(orderDetails=order).count()
            total_quantity = OrderItemMapping.objects.filter(orderDetails=order).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0

    return {'totalitem': totalitem, 'total_quantity': total_quantity}