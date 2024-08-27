from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from books.models import ItemDetails

def viewcart(request):
    con={
        'about':ItemDetails.objects.get(pk=1)
    }
    print(ItemDetails.objects.get(pk=1).description)
    # productDetails=[{
    #     "name":"phyiscs",
    #     "qty":2,
    #     "amount":"$ "+ str(180),
    #     "total_amount":"$ "+ str(360),
    #     "image":"2.jpg",
    #     "index":0

    # },
    # {
    #     "name":"science",
    #     "qty":3,
    #     "amount":"$ "+ str(180),
    #     "total_amount":"$ "+ str(180),
    #     "image":"3.jpg",
    #     "index":1

    # }
    # ]
    # data={"cartInfo":productDetails}
    return render(request,'checkout/viewcart.html',{})

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