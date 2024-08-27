from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from books.models import ItemDetails
from .models import OrderItemMapping,OrderDetails

def viewcart(request):
    field_names = [field.name for field in OrderItemMapping._meta.get_fields()]

    print(field_names)
    query="""SELECT "checkout_orderitemmapping"."id","books_itemdetails"."name",
    "checkout_orderitemmapping"."amount" as total_amount,"books_itemdetails"."image",
    "checkout_orderitemmapping"."quantity" as qty FROM "checkout_orderitemmapping" INNER JOIN "checkout_orderdetails" 
    ON ("checkout_orderitemmapping"."orderDetails_id" = "checkout_orderdetails"."id") 
    INNER JOIN "books_itemdetails" ON ("checkout_orderitemmapping"."itemDetails_id" = "books_itemdetails"."id")
    where "checkout_orderdetails"."status"='In Progress'"""
    # query= """select * from checkout_OrderItemMapping where orderDetails='physics'"""
    data = OrderItemMapping.objects.raw(query)
    for i in data:
        print(i.image)

    return render(request,'checkout/viewcart.html',{"cartInfo":data})

def checkout(request):
    return render(request,'checkout/checkout.html')
def ordersummary(request):
    productDetails=[{
        "name":"phyiscs",
        "qty":2,
        "amount":"$ "+ str(180),
        "total_amount":"$ "+ str(360),
        "image":"2.jpg",
        "index":0

    },
    {
        "name":"science",
        "qty":3,
        "amount":"$ "+ str(180),
        "total_amount":"$ "+ str(180),
        "image":"3.jpg",
        "index":1

    }
    ]
    data={"cartInfo":productDetails}
    return render(request,'checkout/ordersummary.html',data)