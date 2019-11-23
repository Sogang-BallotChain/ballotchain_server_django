from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from . import models
from user.models import User
from userballot.models import UserBallot, UserBallotRegister
from .models import Ballot

from eth_account import Account
from web3 import Web3, HTTPProvider
from .eth.interface import Deployer, BallotContract, requestGas
from .eth import config

import json
import datetime

# uri vote/register/
@csrf_exempt
def register_vote (request):
    if request.method == "POST":
        try:
            # Field check
            req_json = json.loads(request.body.decode("utf-8"))

            email = req_json.get('email', None)
            name = req_json.get('name', None)
            candidate_list = req_json.get('candidate_list', None)
            start_time = req_json.get('start_time', None)
            end_time = req_json.get('end_time', None)

            if ( not email or not name or not candidate_list or not start_time or not end_time ):
                return JsonResponse({"success": 0, "message": "Incorrect json body"})
            
            # Find user with email
            rows  = User.objects.filter(email = email)
            if (len(rows) <= 0):
                return JsonResponse({"success": 0, "message": "No such user"})
            user = rows[0]

            # Get gas from faucet
            request_gas = requestGas(user.eth_pub_key)
            if (request_gas == 0):
                return JsonResponse({"success": 0, "message": "Faucet error"})

            # Deploy bollot to block chain
            deployer = Deployer(len(candidate_list), start_time, end_time)
            address = deployer.deploy(user.eth_prv_key)

            # Create new ballot
            ballot  = Ballot (
                name = name, 
                candidate_list = json.dumps(candidate_list, ensure_ascii=False),
                start_time = start_time,
                end_time = end_time,
                address = address
            )
            ballot.save()

            # User <-> Ballot relation insert
            ubregister = UserBallotRegister(
                user = user,
                ballot = ballot    
            )
            ubregister.save()

            return JsonResponse({"success": 1})
        except (RuntimeError, NameError, ValueError):
            return JsonResponse({"success": 0, "message": "Internal server error"})
    else:
        return JsonResponse({"success": 0, "message": "Use post method instead."})

# uri: vote/{vote_id}
def info (request, vote_id):

    # Find ballot with vote_id
    rows = Ballot.objects.filter(id=vote_id)
    if (len(rows) <= 0):
        return JsonResponse({"success": 0, "message": "No such vote"})
    ballot = rows[0]

    # 투표 시간 지났는지 확인
    is_ended = False
    current_time = datetime.datetime.now().timestamp()
    if (current_time > ballot.end_time):
        is_ended = True

    ballotContract = BallotContract(ballot.address, config.master)
    candidate_list = json.decoder.JSONDecoder().decode(
        rows[0].candidate_list)
    vote_result = {}

    # 투표 결과 컨트랙트 통해 확인
    if (is_ended is False):
        winner = ""
    else:
        winner = candidate_list[ballotContract.getWinner()]
        for i in range(0, len(candidate_list)):
            vote_result[candidate_list[i]] = ballotContract.getVoteCount(i)

    # return json response
    return JsonResponse({
        "success": 1,
        "data": {
            "name": rows[0].name,
            "candidate_list": json.decoder.JSONDecoder().decode(rows[0].candidate_list),
            "start_time": rows[0].start_time,
            "end_time": rows[0].end_time,
            "is_ended": is_ended,
            "winner": winner,
            "result": vote_result
        }
    })

# uri: vote/
@csrf_exempt
def join_vote (request):
    if request.method == "POST":
        try:
            # Field check
            req_json = json.loads(request.body.decode("utf-8"))
            email = req_json.get('email',None)
            vote_id = req_json.get('vote_id',None)
            candidate = req_json.get('candidate',None)

            if ( not email or not vote_id or candidate is None ):
                return JsonResponse({"success": 0, "message": "Incorrect json body."})

            # Find user with email
            rows = User.objects.filter(email=email)
            if (len(rows) <= 0):
                return JsonResponse({"success": 0, "message": "No such user."})
            user = rows[0]

            # Find ballot with vote_id
            rows = Ballot.objects.filter(id=vote_id)
            if (len(rows) <= 0):
                return JsonResponse({"success": 0, "message": "No such ballot."})
            ballot = rows[0]

            # Get gas from faucet
            request_gas = requestGas(user.eth_pub_key)
            if (request_gas == 0):
                return JsonResponse({"success": 0, "message": "Faucet error"})
            
            # Call contract, if fail, then return success 0
            ballotContract = BallotContract(ballot.address, user.eth_prv_key)
            status = ballotContract.vote(candidate)
            if (status == 0):
                return JsonResponse({"success": 0, "message": "Duplicate voting"})

            # User <-> Ballot join relation insert
            userballot = UserBallot(
                user = user,
                ballot = ballot
            )
            userballot.save()
            return JsonResponse({"success": 1})

        except(RuntimeError, NameError):
            return JsonResponse({"success": 0, "message": "Internal server error."})
    else:
        # Field check
        req_json = json.loads(request.body.decode("utf-8"))
        vote_id = req_json.get("vote_id", None)
        if (not vote_id):
            return JsonResponse({"success": 0, "message": "Incorrect json body"})
        
        # Find ballot with vote_id
        rows = Ballot.objects.filter(id=vote_id)
        if (len(rows) <= 0):
            return JsonResponse({"success": 0, "message": "No such vote"})
        ballot = rows[0]

        # 투표 시간 지났는지 확인
        is_ended = False
        current_time = datetime.datetime.now().timestamp()
        if (current_time > ballot.end_time):
            is_ended = True

        ballotContract = BallotContract(ballot.address, config.master)
        candidate_list = json.decoder.JSONDecoder().decode(rows[0].candidate_list)
        vote_result = {}

        # 투표 결과 컨트랙트 통해 확인
        if (is_ended is False):
            winner = ""
        else:
            winner = candidate_list[ballotContract.getWinner()]
            for i in range(0, len(candidate_list)):
                vote_result[candidate_list[i]] = ballotContract.getVoteCount(i)

        # return json response
        return JsonResponse({
            "success": 1,
            "data": {
                "name": rows[0].name,
                "candidate_list": json.decoder.JSONDecoder().decode(rows[0].candidate_list),
                "start_time": rows[0].start_time,
                "end_time": rows[0].end_time,
                "is_ended": is_ended,
                "winner": winner,
                "result": vote_result
            }
        })


# uri /vote/profile/
@csrf_exempt
def profile (request):
    if request.method == "POST":

        try:
            # Field check
            req_json = json.loads(request.body.decode("utf-8"))
            
            flag = req_json.get('flag', None)
            email = req_json.get('email', None)
            page = req_json.get('page', None)
            if (not email or not page or not flag):
                return JsonResponse({"success": 0, "message": "Invalid json body"})

            # Find user with email
            rows = User.objects.filter(email=email)
            if (len(rows) <= 0):
                return JsonResponse({"success": 0, "message": "No such user"})
            user = rows[0]

            # Find User <-> Ballot join relation
            if (flag == "join"):
                rows = UserBallot.objects.filter(user=user)
            # Find User <-> Ballot register relation
            elif (flag == "register"):
                rows = UserBallotRegister.objects.filter(user=user)
            else:
                return JsonResponse({"success": 0, "message": "Flag not defined"})

            if (len(rows) < 0):
                return JsonResponse({"success": 0, "message": "User haven't joined any vote."})

            # pagination
            paginator = Paginator(list(rows), 5)
            try:
                l = paginator.page(page)
            except PageNotAnInteger:
                l = paginator.page(1)
            except EmptyPage:
                l = paginator.page(paginator.num_pages)
            
            data = []
            for i in l:
                data.append(i.ballot.id)

            return JsonResponse({"success": 1, "data": data})
        except (RuntimeError, NameError):
            return JsonResponse({"success": 0, "message": "Internal server error."})
