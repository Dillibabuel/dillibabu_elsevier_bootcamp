from django.shortcuts import render, get_object_or_404
from .models import JournalItemDetails
from django.http import HttpResponse

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

def j_details(request,id):
    #print(id)
    items = get_object_or_404(JournalItemDetails, id=id)
    print("test")
    print(items)
    # return render(request,'journals/j_details.html' ,  {'items': items})
    return render(request,'journals/j_details.html' ,  {'items': items})

def journals_by_category(request, category):
    journals = JournalItemDetails.objects.filter(category=category)
    print(journals)
    return render(request, 'journals/journals.html', {'journals': journals, 'category': category})

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