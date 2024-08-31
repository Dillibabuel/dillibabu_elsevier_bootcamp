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




from django.http import JsonResponse

# def viewcart(request):
#     query="""SELECT "checkout_orderitemmapping"."id","books_itemdetails"."name",
#     "checkout_orderitemmapping"."amount" as total_amount,"books_itemdetails"."image",
#     "checkout_orderitemmapping"."quantity" as qty FROM "checkout_orderitemmapping" INNER JOIN "checkout_orderdetails" 
#     ON ("checkout_orderitemmapping"."orderDetails_id" = "checkout_orderdetails"."id") 
#     INNER JOIN "books_itemdetails" ON ("checkout_orderitemmapping"."itemDetails_id" = "books_itemdetails"."id")
#     where "checkout_orderdetails"."status"='In Progress'"""
#     # query= """select * from checkout_OrderItemMapping where orderDetails='physics'"""
#     data = OrderItemMapping.objects.raw(query)
#     totalitem=len(data)
#     totalproduct=0
#     totalamount=0
#     for item in data:
#         print(item.image.url)  # Debug print to verify
#     for i in data:
#         totalamount+=i.total_amount
#         totalproduct+=i.qty
#     if(request.method=="POST"):
#         mapid=request.POST.get("mapid")
#         OrderItemMapping.objects.filter(id=mapid).delete()


#     return render(request,'checkout/viewcart.html',{"cartInfo":data,"totalitem":totalitem,"totalamount":totalamount,"totalproduct":totalproduct})



def viewcart(request):
    
    user_id = request.user.id  # Assuming the user is logged in and you have the user ID

    # Get the order in progress for the current user
    order = OrderDetails.objects.filter(userid=user_id, status='In Progress').first()

    if not order:
        # If no order in progress, return an empty cart
        return render(request, 'checkout/viewcart.html', {"cartInfo": [], "totalitem": 0, "totalamount": 0, "totalproduct": 0})

    # Get the items in the order
    order_items = OrderItemMapping.objects.filter(orderDetails=order).select_related('itemDetails')

    totalitem = len(order_items)
    totalproduct = sum(item.quantity for item in order_items)
    totalamount = sum(item.amount for item in order_items)

    if request.method == "POST":
        mapid = request.POST.get("mapid")
        OrderItemMapping.objects.filter(id=mapid).delete()
        return redirect('viewcart')  # Redirect back to the viewcart view to refresh the page
    
    return render(request, 'checkout/viewcart.html', {"cartInfo": order_items, "totalitem": totalitem, "totalamount": totalamount, "totalproduct": totalproduct})

# def checkout(request):
#     query="""SELECT "checkout_orderitemmapping"."id","books_itemdetails"."name",
#     "checkout_orderitemmapping"."amount" as total_amount,"books_itemdetails"."image",
#     "checkout_orderitemmapping"."quantity" as qty FROM "checkout_orderitemmapping" INNER JOIN "checkout_orderdetails" 
#     ON ("checkout_orderitemmapping"."orderDetails_id" = "checkout_orderdetails"."id") 
#     INNER JOIN "books_itemdetails" ON ("checkout_orderitemmapping"."itemDetails_id" = "books_itemdetails"."id")
#     where "checkout_orderdetails"."status"='In Progress'"""
#     # query= """select * from checkout_OrderItemMapping where orderDetails='physics'"""
#     data = OrderItemMapping.objects.raw(query)
#     totalitem=len(data)
#     totalproduct=0
#     totalamount=0
#     for i in data:
#         totalamount+=i.total_amount
#         totalproduct+=i.qty
#     if(request.method=="POST"):
#         address=request.POST.get("address")
#         Area=request.POST.get("Area")
#         City=request.POST.get("City")
#         State=request.POST.get("State")
#         PinCode=request.POST.get("PinCode")
#         Country=request.POST.get("Country")
#         COD=request.POST.get("COD")
#         data={
#             "address":address,
#             "Area":Area,
#             "City":City,
#             "State":State,
#             "Pincode":PinCode,
#             "Country":Country
#         }
#         payment=""
#         if COD!=None:
#             payment="Cash On Delivery"
#         else:
#             payment="Card"
#         # print("kalai")
#         orderdata=OrderDetails.objects.raw("select * from checkout_OrderDetails where status=='In Progress'")
        
#         OrderDetails.objects.filter(id=orderdata[0].id).update(address=data,paymenttype=payment,status="Completed")
        

#     return render(request,'checkout/checkout.html',{"totalitem":totalitem,"totalamount":totalamount,"totalproduct":totalproduct})

def checkout(request):
    user_id = request.user.id  # Assuming the user is logged in and you have the user ID

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

        # Get the order in progress for the current user
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

# def ordersummary(request,id):
#     # print('naaz')
#     # print(id)
#     order = OrderDetails.objects.filter(id=id).first()
#     order_items = OrderItemMapping.objects.filter(orderDetails=order)
#     createserver(order,order_items)
#     return render (request,'checkout/ordersummary.html', {"order":order,"order_items":order_items})

def ordersummary(request,id):
    user = request.user
    order = OrderDetails.objects.get(id=id, userid=user.id, status='Completed')
    order_items = OrderItemMapping.objects.filter(orderDetails=order).select_related('itemDetails')
    order_items_dict = []
    for item in order_items:
        item_dict = model_to_dict(item)
        item_dict['single_amount'] = item.amount / item.quantity if item.quantity else 0
        item_dict['item_name'] = item.itemDetails.name  # Add item name to the dictionary
        item_dict['image_url'] = item.itemDetails.image.url  # Add image URL to the dictionary
        order_items_dict.append(item_dict)
    # Send the order confirmation email
    createserver(user, order, order_items)

    return render(request, 'checkout/ordersummary.html', {"order":order,"order_items":order_items_dict})



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
        
        # Update the amount
        order_item.amount = order_item.quantity * item.amount 
        order_item.save()
        # messages.success(request, "Item added to cart successfully!")
        return redirect('books')  # Assuming 'books' is the name of the URL pattern for books.html

    # messages.error(request, "Invalid request")
    return redirect('books')  
        
def createserver(user,order,orderitems):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('mnaazismail5667@gmail.com', 'vmiaaltickbehvqh')
        
        # Create the email
    msg = MIMEMultipart()
    msg['From'] = 'mnaazismail5667@gmail.com'
    msg['To'] = user.email
    msg['Subject'] = 'Request for leave'
        
        # Add the email body
    text = 'Hi how are you'
    order_items_dict = []
    total=0
    for item in orderitems:
        item_dict = model_to_dict(item)
        item_dict['single_amount'] = item.amount / item.quantity if item.quantity else 0
        total+=item.amount
        item_dict['item_name'] = item.itemDetails.name  # Add item name to the dictionary
        item_dict['image_url'] = item.itemDetails.image.url  # Add image URL to the dictionary
        order_items_dict.append(item_dict)
    content=render_to_string('email.html',{"order":order,"order_items":order_items_dict,"total":total})
    msg.attach(MIMEText(content, 'html'))

    pdf_path = 'C:/Users/naazm/django/order.pdf'  # Replace with the actual path to your PDF
    with open(pdf_path, 'rb') as pdf_file:
        pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename=f"order_{order.id}.pdf")
        msg.attach(pdf_attachment)
        
        # Send the email
    server.send_message(msg)
    server.quit()
    print("Email sent successfully")
