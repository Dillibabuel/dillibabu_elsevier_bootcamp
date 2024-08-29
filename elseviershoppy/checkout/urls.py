from django.urls import path,include
from . import views
urlpatterns = [
   path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
   path('',views.viewcart,name='viewcart'),
   path('checkout/',views.checkout,name='checkout'),
   path('ordersummary/',views.ordersummary,name='ordersummary'),
]