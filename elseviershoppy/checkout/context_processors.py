from .models import OrderDetails, OrderItemMapping

def cart_item_count(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        order = OrderDetails.objects.filter(userid=user_id, status='In Progress').first()
        if order:
            totalitem = OrderItemMapping.objects.filter(orderDetails=order).count()
        else:
            totalitem = 0
    else:
        totalitem = 0

    return {'totalitem': totalitem}