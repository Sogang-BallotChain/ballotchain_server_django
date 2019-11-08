from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth

from . import models
from user.models import User
from userballot.models import UserBallot
from .models import Ballot

import json
import datetime

# join <- 투표 참여 확인 <-(컨트랙트 호출)
# new <- 투표 모델 생성 <- (컨트랙트 배포)
# 참여한 투표 조회 

@csrf_exempt
def register_vote (request):
    if request.method == "POST":
        try:
            req_json = json.loads(request.body.decode("utf-8"))

            name = req_json['name']
            candidate_list = req_json['candidate_list']
            start_time = req_json['start_time']
            end_time = req_json['end_time']

            ballot  = Ballot (
                name = name, 
                candidate_list = json.dumps(candidate_list),
                start_time = start_time,
                end_time = end_time
            )
            
            ballot.save()
            # jsonDec = json.decoder.JSONDecoder()
            # l = jsonDec.decode(ballot.candidate_list)
            # str1 = datetime.datetime.fromtimestamp(start_time)
            return JsonResponse({"message": "Hello world"})
        except (RuntimeError, NameError):
            return JsonResponse({"success": 0})

@csrf_exempt
def join_vote (request):
    if request.method == "POST":
        req_json = json.loads(request.body.decode("utf-8"))

        email = req_json.get('email',None)
        vote_id = req_json.get('vote_id',None)
        candidate = req_json.get('candidate',None)

        rows = User.objects.filter(email=email)
        user = rows[0]

        rows = Ballot.objects.filter(id=vote_id)
        ballot = rows[0]

        if (email and vote_id and candidate):
           # print("Here",flush= False)
            userballot = UserBallot(
                user = user,
                ballot = ballot
            )
            userballot.save()
        # email
        # 투표 아이디
        # 누구한테 
        return JsonResponse({"success": 1})
    else:
        return JsonResponse({"success": 0})

@csrf_exempt
def profile (request):
    if request.method == "POST":
        req_json = json.loads(request.body.decode("utf-8"))
        email = req_json.get('email',None)

        rows = User.objects.filter(email=email)
        user = rows[0]

        rows = UserBallot.objects.filter(user=user)
        print(type(rows))
        for v in list(rows):
            print(v,flush = True,sep = ' ')
        return JsonResponse({"success": 1})