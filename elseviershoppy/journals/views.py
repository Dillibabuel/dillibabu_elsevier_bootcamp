from django.shortcuts import render, get_object_or_404
from .models import JournalItemDetails
from django.http import HttpResponse

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from email.mime.application import MIMEApplication

def journals(request):
    journallistdata = JournalItemDetails.objects.all().order_by('name')
    jdata = {"journallistdata": journallistdata}
    if(request.method=="POST"):
        category=request.POST.get("category")
        if category == "all":
            journallistdata = JournalItemDetails.objects.all().order_by('name')
        else:
            journallistdata = JournalItemDetails.objects.filter(category=category).all().order_by('name')
        jdata = {"journallistdata": journallistdata}
    return render(request,'journals/journals.html', jdata)

def j_details(request,id,user):
    #print(id)
    items = get_object_or_404(JournalItemDetails, id=id)
    if request.method=="POST":
        createserver(items,user)
    print("test")
    print(items)
    # return render(request,'journals/j_details.html' ,  {'items': items})
    return render(request,'journals/j_details.html' ,  {'items': items})

def journals_by_category(request, category):
    journals = JournalItemDetails.objects.filter(category=category)
    print(journals)
    return render(request, 'journals/journals.html', {'journals': journals, 'category': category})


def createserver(journals,user):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('mnaazismail5667@gmail.com', 'ycmafanmzixdphkt')
    msg = MIMEMultipart()
    msg['From'] = 'mnaazismail5667@gmail.com'
    msg['To'] = user.email
    msg['Subject'] = 'Request for leave'
        
        # Add the email body
    text = 'Hi how are you'
    # order_items_dict = []
    # total=0
    # for item in orderitems:
    #     item_dict = model_to_dict(item)
    #     item_dict['single_amount'] = item.amount / item.quantity if item.quantity else 0
    #     total+=item.amount
    #     item_dict['item_name'] = item.itemDetails.name  # Add item name to the dictionary
    #     item_dict['image_url'] = item.itemDetails.image.url  # Add image URL to the dictionary
    #     order_items_dict.append(item_dict)
    # content=render_to_string('email.html',{"order":order,"order_items":order_items_dict,"total":total})
    msg.attach(MIMEText(text, 'plain'))

    pdf_path = 'C:/Users/rka/Django_project/'+journals.name+'.pdf'
    print("daf")
    print(pdf_path)  # Replace with the actual path to your PDF
    with open(pdf_path, 'rb') as pdf_file:
        pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename=journals.name)
        msg.attach(pdf_attachment)
        
        # Send the email
    server.send_message(msg)
    server.quit()
    print("Email sent successfully")
# def books(request):
#     booklistdata = ItemDetails.objects.all().order_by('name')
#     data = {"bookdata": booklistdata}
#     if(request.method=="POST"):
#         category=request.POST.get("category")
#         if category == "all":
#             booklistdata = ItemDetails.objects.all().order_by('name')
#         else:
#             booklistdata = ItemDetails.objects.filter(category=category).all().order_by('name')
#         data = {"bookdata": booklistdata}
#         # print(data)
   
#     return render(request, 'books/books.html', data)