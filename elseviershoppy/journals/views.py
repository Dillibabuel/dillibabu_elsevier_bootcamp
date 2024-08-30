from django.shortcuts import render, get_object_or_404
from .models import JournalItemDetails
from django.http import HttpResponse

def journals(request):
    journallistdata = JournalItemDetails.objects.all()
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

