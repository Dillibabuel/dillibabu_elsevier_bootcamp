from django.urls import path,include
from . import views
urlpatterns = [
   path('',views.viewcart),
   path('checkout/',views.checkout),
   path('ordersummary/',views.ordersummary),
]