from django.conf.urls import url

from . import views

urlpatterns = [
    url('(?P<student_id>\d+)', views.testfunc, name="testfunc"),
	url('', views.index, name='index')
]
