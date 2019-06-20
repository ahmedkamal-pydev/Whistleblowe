from django.contrib import admin
from webapp.models import Location, Department, Attachment, ReportType, Report, Administrator, Reporter, Feedback
# Register your models here.

admin.site.register(Reporter)
admin.site.register(Feedback)
admin.site.register(Administrator)
admin.site.register(Report)
admin.site.register(ReportType)
admin.site.register(Attachment)
admin.site.register(Department)
admin.site.register(Location)
