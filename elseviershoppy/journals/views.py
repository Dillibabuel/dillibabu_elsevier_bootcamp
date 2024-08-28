# from django.shortcuts import render

# # Create your views here.
# from django.http import HttpResponse
# def journals(request):
#     return render(request,'journals.html')
from django.shortcuts import render
from .models import JournalItemDetails
from django.http import HttpResponse

def journals(request):
    journallistdata = JournalItemDetails.objects.all()
    for i in journallistdata:
        print(i.image)
    jdata = {"journaldata": journallistdata}
    return render(request,'journals/journals.html', jdata)

def j_details(request):
    return render(request,'journals/j_details.html')
    




