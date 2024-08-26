from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def viewcart(request):
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
    return render(request,'checkout/viewcart.html',data)

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