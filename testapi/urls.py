from django.conf.urls import url

from . import views

urlpatterns = [
    #url('', views.index, name='index'),
    url('(?P<student_id>\d+)', views.testfunc, name="testfunc")
]