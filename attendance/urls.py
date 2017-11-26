from django.conf.urls import url
from . import views


app_name = 'attendance'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^schools/$', views.SchoolListView.as_view(), name='school_list'),
    url(r'^about/$', views.AboutView, name='about'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^teacher/(?P<pk>[0-9]+)/$', views.TeacherDetailView.as_view(), name='profile'),
    url(r'^teacher/(?P<pk>[0-9]+)/update/$', views.TeacherUpdateView.as_view(), name='profile_update'),
    url(r'^student/(?P<pk>[0-9]+)/$', views.StudentDetailView.as_view(), name='student_detail'),
    url(r'^teacher/(?P<pk>[0-9]+)/create_student/$', views.create_student, name='student_create'),
    url(r'^teacher/(?P<pk>[0-9]+)/attendance/$', views.mark_attendance, name='mark_attendance'),
    url(r'^principal/(?P<pk>[0-9]+)/$', views.SchoolDetailView.as_view(), name='school_detail'),
    url(r'^report/(?P<pk>[0-9]+)/attendance/$', views.attendance_report, name='attendance_report'),
    url(r'^report/(?P<pk>[0-9]+)/attendance/download/$', views.export_to_csv, name='export_to_csv'),
]