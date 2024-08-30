from django.urls import path,include
from . import views
urlpatterns = [
   path('',views.journals, name='journals'),
   path('journal/<int:id>/',views.j_details, name='j_details'),
   path('journal/<str:category>/',views.journals, name='journals'),
   # path('journals/<str:category_name>/', views.journals_by_category, name='journals_by_category'),
]