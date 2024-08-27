from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from books.models import ItemDetails
from .models import OrderItemMapping,OrderDetails

def viewcart(request):
    query="""SELECT "checkout_orderitemmapping"."id","books_itemdetails"."name",
    "checkout_orderitemmapping"."amount" as total_amount,"books_itemdetails"."image",
    "checkout_orderitemmapping"."quantity" as qty FROM "checkout_orderitemmapping" INNER JOIN "checkout_orderdetails" 
    ON ("checkout_orderitemmapping"."orderDetails_id" = "checkout_orderdetails"."id") 
    INNER JOIN "books_itemdetails" ON ("checkout_orderitemmapping"."itemDetails_id" = "books_itemdetails"."id")
    where "checkout_orderdetails"."status"='In Progress'"""
    # query= """select * from checkout_OrderItemMapping where orderDetails='physics'"""
    data = OrderItemMapping.objects.raw(query)
    if(request.method=="POST"):
        mapid=request.POST.get("mapid")
        OrderItemMapping.objects.filter(id=mapid).delete()


    return render(request,'checkout/viewcart.html',{"cartInfo":data})

def checkout(request):
    if(request.method=="POST"):
        address=request.POST.get("address")
        Area=request.POST.get("Area")
        City=request.POST.get("City")
        State=request.POST.get("State")
        PinCode=request.POST.get("PinCode")
        Country=request.POST.get("Country")
        COD=request.POST.get("COD")
        data={
            "address":address,
            "Area":Area,
            "City":City,
            "State":State,
            "Pincode":PinCode,
            "Country":Country
        }
        payment=""
        if COD!=None:
            payment="Cash On Delivery"
        else:
            payment="Card"
        print("kalai")
        orderdata=OrderDetails.objects.raw("select * from checkout_OrderDetails where status=='In Progress'")
        
        OrderDetails.objects.filter(id=orderdata[0].id).update(address=data,paymenttype=payment)
        print(OrderDetails.objects.filter(id=orderdata[0].id))
        

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