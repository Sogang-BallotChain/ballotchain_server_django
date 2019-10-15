# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def testfunc(request, student_id):
    response = "Not found"
    print(student_id)
    if student_id == "20161596":
        response = "Seo Hyungyu"
    return HttpResponse(response)