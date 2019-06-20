from django.conf.urls import url
from webapp import views

app_name = 'webapp'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^usersignup/$', views.UserSignUpView, name='usersignup'),
    url(r'^usersignin/$', views.UserSignInView, name='usersignin'),
    url(r'^userhomepage/$', views.UserHomepageView, name='userhomepage'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserReportDetailsView, name='userreportdetails'),
    url(r'^usercreatereport/$', views.UserCreateReportView, name='usercreatereport'),
    url(r'^signout/$', views.SignOutView, name='signout'),
    url(r'^adminsignin/$', views.AdminSignInView, name='adminsignin'),
    url(r'^adminhomepage/$', views.AdminHomepageView, name='adminhomepage'),
    url(r'^adminhomepage/i/$', views.AdminImportantView, name='adminimportant'),
    url(r'^adminhomepage/n/$', views.AdminNormalView, name='adminnormal'),
    url(r'^admin/(?P<pk>[0-9]+)/$', views.AdminReportDetailsView, name='adminreportdetails'),
    url(r'^(?P<pk>[0-9]+)/$', views.CategorizeReportView, name='categorizereport'),
    url(r'^adminhomepage/s/$', views.AdminSpamView, name='adminspam'),
    url(r'^adminhomepage/r/$', views.AdminReadView, name='adminread'),
    url(r'^createfeedback/$', views.CreateFeedbackView.as_view(), name='createfeedback'),
]
