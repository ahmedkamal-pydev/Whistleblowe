from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse

# Create your models here.

phone_regex = '^03\d{2}\W\d{7}$'

class Reporter(models.Model):
    reporter_id = models.AutoField(primary_key=True)
    user_reporter = models.OneToOneField(User)
    age = models.PositiveSmallIntegerField()
    phone_no = models.CharField(max_length=12, unique=True, validators = [RegexValidator(regex=phone_regex,
                                                                                                    message='Phone number must be in the format xxxx-xxxxxxx',
                                                                                                    code='Invalid phone number!')])

    class Meta:
        db_table = 'Reporter'

    def __str__(self):
        return self.user_reporter.username

    def get_absolute_url(self):
        return reverse("index")

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=20)
    province = models.CharField(max_length=20)

    class Meta:
        db_table = 'Location'

    def __str__(self):
        return self.city

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=50)
    admin = models.ForeignKey('Administrator')

    class Meta:
        db_table = 'Department'

    def __str__(self):
        return self.department_name

class Attachment(models.Model):
    attachment_id = models.AutoField(primary_key=True)
    attachments = models.FileField(upload_to='attachments', blank=True, null=True)
    report = models.ForeignKey('Report', blank=True, null=True)

    class Meta:
        db_table = 'Attachment'

class ReportType(models.Model):
    report_type_id = models.AutoField(primary_key=True)
    report_type = models.CharField(max_length=20)
    identity = models.CharField("crime/illegal activity", max_length=20)

    class Meta:
        db_table = 'Report Type'

    def __str__(self):
        return self.identity

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    report_type = models.ForeignKey('ReportType', related_name='reports')
    department = models.ForeignKey('Department', related_name='reports')
    location = models.ForeignKey('Location', related_name='reports')
    reporter = models.ForeignKey('Reporter')
    add_evidence = models.CharField("additional evidence", max_length=500, blank=True, null=True)
    status = models.CharField(max_length=10, default='pending')
    report_date = models.DateField(_("Date"), auto_now_add=True)

    class Meta:
        db_table = 'Report'
        ordering = ['-report_date']

    def __str__(self):
        return self.report_type.identity

class Administrator(models.Model):
    administrator_id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(User)

    class Meta:
        db_table = 'Administrator'

    def __str__(self):
        return self.admin.username

class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    feedback = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.feedback_id)

    def get_absolute_url(self):
        return reverse("index")
