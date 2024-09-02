import csv
from django.http import HttpResponse

def export_as_csv(modeladmin, request, queryset):
    """
    Generic csv export admin action.
    """
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment;filename={opts.verbose_name}.csv'
    writer = csv.writer(response)

    field_names = [field.name for field in opts.fields]
    writer.writerow(field_names)

    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response

export_as_csv.short_description = "Export Selected as CSV"