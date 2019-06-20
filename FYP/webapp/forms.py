from django import forms
from webapp.models import Reporter, Attachment, Location, Department, ReportType, Report, Administrator, Feedback
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')


class ReporterForm(forms.ModelForm):
    class Meta():
        model = Reporter
        fields = ('age', 'phone_no')


class DepartmentForm(forms.ModelForm):
    department = forms.ModelChoiceField(required=True, queryset = Department.objects.all(), widget=forms.Select() )

    class Meta:
        model = Department
        fields = ('department',)


class LocationForm(forms.ModelForm):
    location = forms.ModelChoiceField(required=True, queryset = Location.objects.all(), widget=forms.Select() )

    class Meta:
        model = Location
        fields = ('location',)


class ReportTypeForm(forms.ModelForm):
    identity = forms.ModelChoiceField(required=True, queryset = ReportType.objects.all(), widget=forms.Select() )

    class Meta:
        model = ReportType
        fields = ('identity',)


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('attachments',)


class ReportForm(forms.ModelForm):
    add_evidence = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Report
        fields = ('add_evidence',)


class AdministratorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class FeedbackForm(forms.ModelForm):
    feedback = forms.CharField()

    class Meta:
        model = Feedback
        fields = ('feedback',)
