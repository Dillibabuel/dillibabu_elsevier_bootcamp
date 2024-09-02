from django.shortcuts import render, get_object_or_404
from .models import JournalItemDetails
from django.http import HttpResponse
import smtplib
from django.contrib import messages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from email.mime.application import MIMEApplication
from checkout.models import OrderDetails, OrderItemMapping
from django.db.models import Sum

def journals(request):
    user_id = request.user.id
    order = OrderDetails.objects.filter(userid=user_id, status='In Progress').first()

    total_quantity = 0
    if order:
        total_quantity = OrderItemMapping.objects.filter(orderDetails=order).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0
    
    journallistdata = JournalItemDetails.objects.all().order_by('name')
    jdata = {"journallistdata": journallistdata,"total_quantity": total_quantity}
    
    if(request.method=="POST"):
        category=request.POST.get("category")
        if category == "all":
            journallistdata = JournalItemDetails.objects.all().order_by('name')
        else:
            journallistdata = JournalItemDetails.objects.filter(category=category).all().order_by('name')
        jdata = {"journallistdata": journallistdata,"total_quantity": total_quantity}
    return render(request,'journals/journals.html', jdata)

def j_details(request,id):

    user_id = request.user.id
    order = OrderDetails.objects.filter(userid=user_id, status='In Progress').first()

    total_quantity = 0
    if order:
        total_quantity = OrderItemMapping.objects.filter(orderDetails=order).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0
    user = request.user
    items = get_object_or_404(JournalItemDetails, id=id)
    if request.method=="POST":
        createserver(request,items,user)
    print("test")
    print(items)
    # return render(request,'journals/j_details.html' ,  {'items': items})
    return render(request,'journals/j_details.html' ,  {'items': items,'user': user,'total_quantity':total_quantity})

def journals_by_category(request, category):
    journals = JournalItemDetails.objects.filter(category=category)
    print(journals)
    return render(request, 'journals/journals.html', {'journals': journals, 'category': category})


def createserver(request,journals,user):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('mnaazismail5667@gmail.com', 'lyhoutbjnweqczpk')
    msg = MIMEMultipart()
    msg['From'] = 'akshathamayya23@gmail.com'
    msg['To'] = 'akshathamayya23@gmail.com'
    msg['Subject'] = 'Requested Journal'
        
        # Add the email body
    text = 'Thank you for your recent purchase from ElsevierShoppy, our dedicated e-commerce platform for accessing a wide range of academic journals and publications.'

    msg.attach(MIMEText(text, 'plain'))

    pdf_path = 'C:/Users/rka/Django_project/'+journals.name+'.pdf'
    print("daf")
    print(pdf_path)  # Replace with the actual path to your PDF
    with open(pdf_path, 'rb') as pdf_file:
        pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename=journals.name)
        msg.attach(pdf_attachment)

    server.send_message(msg)
    messages.success(request, 'Mailed Successfully !')
    server.quit()
    print("Email sent successfully")
    
