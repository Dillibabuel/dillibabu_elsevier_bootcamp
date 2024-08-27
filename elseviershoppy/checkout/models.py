from django.db import models
from books.models import ItemDetails
from django.utils import timezone

class OrderDetails(models.Model):
    id = models.AutoField(primary_key=True)
    userid=models.IntegerField(default=1)
    address=models.JSONField(default=dict())
    paymenttype=models.CharField(max_length=100,blank=False,default="")
    status=models.CharField(max_length=100,blank=False,default="")
    date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)
    
class OrderItemMapping(models.Model):
    id = models.AutoField(primary_key=True)
    orderDetails=models.ForeignKey(OrderDetails, on_delete = models.CASCADE) 
    itemDetails=models.ForeignKey(ItemDetails, on_delete = models.CASCADE) 
    quantity=models.IntegerField(default=0)
    amount=models.IntegerField(default=0)
    def __str__(self):
        return str(self.id)+"-"+str(self.itemDetails)
    

# Create your models here.
