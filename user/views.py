from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth

from . import models
import json

from web3 import Web3, HTTPProvider
from vote.eth import config

#signup
@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            # Parse body
            req_json = json.loads(request.body.decode("utf-8"))

            # Field check
            email = req_json.get('email', None)
            password = req_json.get('password', None)

            if (not email or not password):
                return JsonResponse({"success" : 0, "message": "Invalid json body"})

            # Duplicate user
            row = models.User.objects.filter(email = req_json['email'])
            if (len(row) > 0):
                return JsonResponse({"success": 0, "message": "Duplicate user"})

            # Make public key and private key
            w3 = Web3(HTTPProvider(config.rpc_url))
            account = w3.eth.account.create(password)
            pub_key = account.address
            prv_key = account.privateKey.hex()
            #pub_key = w3.geth.personal.newAccount(password)
            
            # Create new user 
            user = models.User(
                email = email, 
                password = password, 
                eth_pub_key = pub_key, 
                eth_prv_key = prv_key
            )
            user.save()

            return JsonResponse({"success": 1}, status=200)
        except (RuntimeError, NameError):
            return JsonResponse({"success": 0, "message": "Server error"})
        except (json.decoder.JSONDecodeError):
            return JsonResponse({"success": 0, "message": "Need json body"})
    
    return JsonResponse({"success": 0, "message": "Use post method instead."})

#signin
@csrf_exempt
def signin(request):
    if (request.method == "POST"):
        try:
            #TODO: check fields

            # check user sign up
            req_json = json.loads(request.body.decode("utf-8"))
            rows = models.User.objects.filter(email = req_json["email"], password = req_json["password"])
            if (len(rows) <= 0):
                return JsonResponse({"success": 0, "message": "No user with such email."})
            else:
                return JsonResponse({"success": 1})
        except (RuntimeError, NameError):
            return JsonResponse({"success": 0, "message": "Server error"})

    return JsonResponse({"success": 0, "message": "Use post method instead"})


#signout
@csrf_exempt
def signout(request):

    if (request.method == "POST"):
        return JsonResponse({"success": 1})
        
    return JsonResponse({"success": 0, "message": "Use post method instead"})