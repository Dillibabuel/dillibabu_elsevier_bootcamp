
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.books,name='books'),
    path('book/<int:id>/',views.booksdetails,name='booksdetails'),

]
