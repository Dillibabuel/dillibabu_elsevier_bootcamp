# from django.db import models

# # Create your models here.
from django.db import models

# Create your models here.
class JournalItemDetails(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=30,blank=False,default="")
    # amount=models.IntegerField(blank=False)
    category=models.CharField(max_length=30,blank=False,default="")
    description = models.TextField(max_length=200,blank=False)
    image=models.ImageField(upload_to='journals/',blank=False)
    def __str__(self):
        return str(self.name)
