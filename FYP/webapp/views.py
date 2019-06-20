from webapp.forms import AttachmentForm, ReportForm, UserForm, ReporterForm, DepartmentForm, LocationForm, ReportTypeForm
from webapp.models import Reporter, Location, Department, Attachment, ReportType, Report, Administrator, Feedback

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import datetime
from django.utils import timezone

from django.views.generic import TemplateView, CreateView

#VIEWS FOR USERS

#INDEX PAGE
class IndexView(TemplateView):
    template_name = 'index.html'



#SIGN UP PAGE
def UserSignUpView(request):
    signup = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        reporter_form = ReporterForm(data=request.POST)

        if user_form.is_valid() and reporter_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            reporter = reporter_form.save(commit=False)
            reporter.user_reporter = user

            reporter.save()

            signup = True
        else:
            print(user_form.errors, reporter_form.errors)

    else:
         user_form = UserForm()
         reporter_form = ReporterForm()

    return render(request,'usersignup.html',
                          {'user_form':user_form,
                           'reporter_form':reporter_form,
                           'signup':signup})



#USER SIGN IN PAGE
def UserSignInView(request):
    response = redirect('/webapp/userhomepage')

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return response
            else:
                return HttpResponse("Account Not Active")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'usersignin.html', {})



#USER HOMEPAGE
@login_required
def UserHomepageView(request):
    id = request.user.id
    user = User.objects.get(pk=id)
    viewer = Reporter.objects.get(user_reporter_id=user.id)

    try:
        rep = Report.objects.filter(reporter=viewer).exclude(status='cleared')
    except Report.DoesNotExist:
        rep = None

    return render(request, 'userhomepage.html', {'rep':rep})



#USER REPORT DETAILS
@login_required
def UserReportDetailsView(request, pk):
    report = get_object_or_404(Report, pk=pk)

    try:
        attach = Attachment.objects.get(report=pk)
    except Attachment.DoesNotExist:
        attach = None

    return render(request, 'userreportdetails.html', {'report':report,
                                                            'attach':attach})



#USER REPORT CREATION
@login_required
def UserCreateReportView(request):
    response = redirect('/webapp/userhomepage')
    submit = False

    att_form = AttachmentForm()
    rep_form = ReportForm()
    dep_form = DepartmentForm()
    loc_form = LocationForm()
    rtp_form = ReportTypeForm()

    if request.method == 'POST':
        att = AttachmentForm(request.POST)
        r = ReportForm(request.POST)
        d = DepartmentForm(request.POST)
        l = LocationForm(request.POST)
        rt = ReportTypeForm(request.POST)

        if att.is_valid() and r.is_valid() and d.is_valid() and l.is_valid() and rt.is_valid():
            l = request.POST.get('location')
            city = Location.objects.get(pk=l)
            d = request.POST.get('department')
            department = Department.objects.get(pk=d)
            c = request.POST.get('identity')
            crime = ReportType.objects.get(pk=c)
            a = request.user.id
            curr_user = User.objects.get(pk=a)
            reporter = Reporter.objects.get(user_reporter_id=curr_user.id)
            r = request.POST.get('add_evidence')
            dat = timezone.now()
            newreport = Report.objects.create(report_type=crime, department=department, location=city, reporter=reporter, add_evidence=r, report_date=dat)

            if 'attachments' in request.FILES:
                att.attachments = request.FILES['attachments']
                attach = Attachment.objects.create(attachments=att.attachments, report=newreport)

            return response

    else:
        att_form = AttachmentForm()
        rep_form = ReportForm()
        dep_form = DepartmentForm()
        loc_form = LocationForm()
        rtp_form = ReportTypeForm()

    return render(request,'usercreatereport.html',
                          {'att_form':att_form,
                           'rep_form':rep_form,
                           'dep_form':dep_form,
                           'loc_form':loc_form,
                           'rtp_form':rtp_form,
                           'submit':submit})



#VIEWS FOR ADMINISTRATOR

#ADMIN SIGN IN PAGE
def AdminSignInView(request):
    response = redirect('/webapp/adminhomepage')

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return response
            else:
                return HttpResponse("Account Not Active")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'adminsignin.html', {})



#ADMIN HOMEPAGE
@login_required
def AdminHomepageView(request):
    try:
        rep = Report.objects.raw("""SELECT report_id, identity, city, department_name From Report INNER JOIN Department on Report.department_id = Department.department_id INNER JOIN Location on Report.location_id = Location.location_id INNER JOIN [Report Type] on Report.report_type_id = [Report Type].[report_type_id] INNER JOIN Administrator on Department.admin_id = Administrator.administrator_id INNER JOIN auth_user on auth_user.id = Administrator.admin_id WHERE auth_user.id = %s AND [Report Type].[report_type] = 'Critical'""" % request.user.id)
    except Report.DoesNotExist:
        rep = None

    return render(request, 'adminhomepage.html', {'rep':rep})



#ADMIN IMPORTANT REPORTS
@login_required
def AdminImportantView(request):
    try:
        rep = Report.objects.raw("""SELECT report_id, identity, city, department_name From Report INNER JOIN Department on Report.department_id = Department.department_id INNER JOIN Location on Report.location_id = Location.location_id INNER JOIN [Report Type] on Report.report_type_id = [Report Type].[report_type_id] INNER JOIN Administrator on Department.admin_id = Administrator.administrator_id INNER JOIN auth_user on auth_user.id = Administrator.admin_id WHERE auth_user.id = %s AND [Report Type].[report_type] = 'Important'""" % request.user.id)
    except Report.DoesNotExist:
        rep = None

    return render(request, 'adminhomepage.html', {'rep':rep})



#ADMIN NORMAL REPORTS
@login_required
def AdminNormalView(request):
    try:
        rep = Report.objects.raw("""SELECT report_id, identity, city, department_name From Report INNER JOIN Department on Report.department_id = Department.department_id INNER JOIN Location on Report.location_id = Location.location_id INNER JOIN [Report Type] on Report.report_type_id = [Report Type].[report_type_id] INNER JOIN Administrator on Department.admin_id = Administrator.administrator_id INNER JOIN auth_user on auth_user.id = Administrator.admin_id WHERE auth_user.id = %s AND [Report Type].[report_type] = 'Normal'""" % request.user.id)
    except Report.DoesNotExist:
        rep = None

    return render(request, 'adminhomepage.html', {'rep':rep})



#ADMIN NORMAL REPORTS
@login_required
def AdminReadView(request):
    try:
        rep = Report.objects.raw("""SELECT report_id, identity, city, department_name From Report INNER JOIN Department on Report.department_id = Department.department_id INNER JOIN Location on Report.location_id = Location.location_id INNER JOIN [Report Type] on Report.report_type_id = [Report Type].[report_type_id] INNER JOIN Administrator on Department.admin_id = Administrator.administrator_id INNER JOIN auth_user on auth_user.id = Administrator.admin_id WHERE auth_user.id = %s AND Report.status = 'read'""" % request.user.id)
    except Report.DoesNotExist:
        rep = None

    return render(request, 'adminread.html', {'rep':rep})



#ADMIN NORMAL REPORTS
@login_required
def AdminSpamView(request):
    try:
        rep = Report.objects.raw("""SELECT report_id, identity, city, department_name From Report INNER JOIN Department on Report.department_id = Department.department_id INNER JOIN Location on Report.location_id = Location.location_id INNER JOIN [Report Type] on Report.report_type_id = [Report Type].[report_type_id] INNER JOIN Administrator on Department.admin_id = Administrator.administrator_id INNER JOIN auth_user on auth_user.id = Administrator.admin_id WHERE auth_user.id = %s AND Report.status = 'spam'""" % request.user.id)
    except Report.DoesNotExist:
        rep = None

    return render(request, 'adminspam.html', {'rep':rep})


#ADMIN REPORT DETAILS
@login_required
def AdminReportDetailsView(request, pk):
    report = get_object_or_404(Report, pk=pk)

    try:
        attach = Attachment.objects.get(report=pk)
    except Attachment.DoesNotExist:
        attach = None

    return render(request, 'adminreportdetails.html', {'report':report,
                                                            'attach':attach})



#CATEGORIZE REPORTS
def CategorizeReportView(request, pk):
    response = redirect('/webapp/adminhomepage')

    if request.method == 'POST':
        if request.POST.get('read'):
            report = get_object_or_404(Report, pk=pk)
            report.status = 'read'
            report.save()
            return response
        elif request.POST.get('spam'):
            report = get_object_or_404(Report, pk=pk)
            report.status = 'spam'
            report.save()
            return response
        elif request.POST.get('cleared'):
            report = get_object_or_404(Report, pk=pk)
            report.status = 'cleared'
            report.save()
            return response

    return render(request, 'adminreportdetails.html', {})


#VIEWS FOR USER AND ADMINISTRATOR

#CREATE FEEDBACK
class CreateFeedbackView(CreateView):
    model = Feedback
    fields = ['feedback']



#SIGNOUT
@login_required
def SignOutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
