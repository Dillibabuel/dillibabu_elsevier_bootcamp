from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse
from books.models import ItemDetails
from .models import OrderItemMapping,OrderDetails
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from email.mime.application import MIMEApplication
from django.db.models import Sum
from django.http import JsonResponse




def viewcart(request):
    
    user_id = request.user.id 

    
    order = OrderDetails.objects.filter(userid=user_id, status='In Progress').first()

    if not order:
        return render(request, 'checkout/viewcart.html', {"cartInfo": [], "totalitem": 0, "totalamount": 0, "totalproduct": 0})

    order_items = OrderItemMapping.objects.filter(orderDetails=order).select_related('itemDetails')

    totalitem = len(order_items)
    totalproduct = sum(item.quantity for item in order_items)
    totalamount = sum(item.amount for item in order_items)
    order_items_dict = []
    for item in order_items:
        item_dict = model_to_dict(item)
        item_dict['single_amount'] = item.amount / item.quantity if item.quantity else 0
        item_dict['item_name'] = item.itemDetails.name  
        item_dict['image_url'] = item.itemDetails.image.url  
        order_items_dict.append(item_dict)

 

    if request.method == "POST":
        mapid = request.POST.get("mapid")
        item = OrderItemMapping.objects.get(id=mapid)
        if item.quantity > 1:
            item.quantity -= 1
            item.amount = item.quantity * item.itemDetails.amount
            item.save()
        else:
            item.delete()
        return redirect('viewcart')   
    
    return render(request, 'checkout/viewcart.html', {"cartInfo": order_items_dict, "totalitem": totalitem, "totalamount": totalamount, "totalproduct": totalproduct})


        


def checkout(request):
    user_id = request.user.id 

    query = """
    SELECT "checkout_orderitemmapping"."id","checkout_orderdetails"."id" as orderid, "books_itemdetails"."name",
    "checkout_orderitemmapping"."amount" as total_amount, "books_itemdetails"."image",
    "checkout_orderitemmapping"."quantity" as qty FROM "checkout_orderitemmapping"
    INNER JOIN "checkout_orderdetails" ON ("checkout_orderitemmapping"."orderDetails_id" = "checkout_orderdetails"."id")
    INNER JOIN "books_itemdetails" ON ("checkout_orderitemmapping"."itemDetails_id" = "books_itemdetails"."id")
    WHERE "checkout_orderdetails"."status"='In Progress' AND "checkout_orderdetails"."userid"=%s
    """
    data = OrderItemMapping.objects.raw(query, [user_id])
    totalitem = len(data)
    totalproduct = sum(item.qty for item in data)
    totalamount = sum(item.total_amount for item in data)

    if request.method == "POST":
        address = {
            "address": request.POST.get("address"),
            "Area": request.POST.get("Area"),
            "City": request.POST.get("City"),
            "State": request.POST.get("State"),
            "PinCode": request.POST.get("PinCode"),
            "Country": request.POST.get("Country")
        }
        payment_type = "COD" if request.POST.get("COD") else "Card"

        order = OrderDetails.objects.filter(userid=user_id, status='In Progress').first()
        print(order)
        orderid = order.id
        if order:
            order.address = address
            order.paymenttype = payment_type
            order.status = 'Completed'
            order.date = timezone.now()
            order.save()

        return redirect(reverse('ordersummary', args=[orderid]))

    return render(request, 'checkout/checkout.html', {"totalitem": totalitem, "totalamount": totalamount, "totalproduct": totalproduct})


def ordersummary(request,id):
    user = request.user
    order = OrderDetails.objects.get(id=id, userid=user.id, status='Completed')
    order_items = OrderItemMapping.objects.filter(orderDetails=order).select_related('itemDetails')
    order_items_dict = []
    for item in order_items:
        item_dict = model_to_dict(item)
        item_dict['single_amount'] = item.amount / item.quantity if item.quantity else 0
        item_dict['item_name'] = item.itemDetails.name  
        item_dict['image_url'] = item.itemDetails.image.url  
        order_items_dict.append(item_dict)

    total_amount = order_items.aggregate(total=Sum('amount'))['total'] or 0

    createserver(user, order, order_items)

    return render(request, 'checkout/ordersummary.html', {"order":order,"order_items":order_items_dict,"total_amount":total_amount})



@login_required
def add_to_cart(request):
    if request.method == "POST":
        book_id = request.POST.get('book_id')
        quantity = int(request.POST.get('quantity', 1))
        
        if not book_id:
            return JsonResponse({"error": "Book ID is required"}, status=400)
        
        try:
            book_id = int(book_id)
        except ValueError:
            return JsonResponse({"error": "Invalid Book ID"}, status=400)
        
        user_id  = request.user
        
        
        order, created = OrderDetails.objects.get_or_create(userid=user_id.id, status='In Progress')
        
        try:
            item = ItemDetails.objects.get(id=book_id)
        except ItemDetails.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)
        
        order_item, created = OrderItemMapping.objects.get_or_create(orderDetails=order, itemDetails=item)
        
        if not created:
            order_item.quantity += quantity
        else:
            order_item.quantity = quantity
        
        
        order_item.amount = order_item.quantity * item.amount 
        order_item.save()
        # messages.success(request, "Item added to cart successfully!")
        return redirect('books')  

    # messages.error(request, "Invalid request")
    return redirect('books')  
        
def createserver(user,order,orderitems):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('mnaazismail5667@gmail.com', 'saazdhgwfsqmvsqr')
        
    
    msg = MIMEMultipart()
    msg['From'] = 'mnaazismail5667@gmail.com'
    msg['To'] = user.email
    msg['Subject'] = 'Order has been confirmed'
        
        
    order_items_dict = []
    total=0
    for item in orderitems:
        item_dict = model_to_dict(item)
        item_dict['single_amount'] = item.amount / item.quantity if item.quantity else 0
        total+=item.amount
        item_dict['item_name'] = item.itemDetails.name
        item_dict['image_url'] = item.itemDetails.image.url 
        order_items_dict.append(item_dict)
    content=render_to_string('email.html',{"order":order,"order_items":order_items_dict,"total":total})
    msg.attach(MIMEText(content, 'html'))

    # pdf_path = 'C:/Users/naazm/django/order.pdf'  
    # with open(pdf_path, 'rb') as pdf_file:
    #     pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
    #     pdf_attachment.add_header('Content-Disposition', 'attachment', filename=f"order_{order.id}.pdf")
    #     msg.attach(pdf_attachment)
        
    server.send_message(msg)
    server.quit()
    print("Email sent successfully")
