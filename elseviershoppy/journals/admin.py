from django.contrib import admin
from .models import JournalItemDetails
# admin.site.register(JournalItemDetails)
from .utils import export_as_csv
@admin.register(JournalItemDetails)
class JournalItemDetailsAdmin(admin.ModelAdmin):
    list_display = ('id','name','author','subscriptioncharge','category','image' ) # Customize your list display
    actions = [export_as_csv]  # Register the export action