import csv
from django.http import HttpResponse
from django.utils.encoding import smart_str

def export_as_csv(modeladmin, request, queryset):
    """
    Generic CSV export function that works for any model.
    """
    model = modeladmin.model
    field_names = [field.name for field in model._meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{model._meta.model_name}.csv"'

    writer = csv.writer(response)
    
    # Write the header row (field names)
    writer.writerow(field_names)

    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response

export_as_csv.short_description = "Export Selected to CSV"
