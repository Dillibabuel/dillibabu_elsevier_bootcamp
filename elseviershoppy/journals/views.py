# from django.shortcuts import render

# # Create your views here.
# from django.http import HttpResponse
# def journals(request):
#     return render(request,'journals.html')
from django.shortcuts import render
from .models import JournalItemDetails
# Create your views here.
from django.http import HttpResponse
def journals(request):
    return render(request,'journals/journals.html')
    
def journals(request):
    journallistdata = JournalItemDetails.objects.all()
    data = {"journaldata": journallistdata}
    return render(request,'journals/journals.html', data)