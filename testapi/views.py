# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def testfunc(request, student_id):

    if request.method == "POST":
        return JsonResponse({'email': "Not found because ...", 'message': 'Post request'})

    response = "Not found"

    if student_id == "20161596":
        response = "omnipede@naver.com"
    elif student_id == "20161616":
        response = "tmd3282@naver.com"
    elif student_id == "20121650":
        response = "yhatonline@naver.com"
    elif student_id == "20141508":
        response = "pineleaf1215@gmail.com"
    return JsonResponse({'email': response, "message": "Hello world!"})
