from django.shortcuts import render
from .models import MyUser
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
# Create your views here.
from rest_framework.decorators import api_view
import jwt
# from jwt import inva
from bcrypt import hashpw, checkpw
from jwt.exceptions import InvalidSignatureError,InvalidAlgorithmError,DecodeError,ExpiredSignatureError
from datetime import datetime, timedelta
@api_view(["POST"])
def register(request):
    data = request.data 
    data["passwod"] = make_password(data["passwod"])
    MyUser.objects.create(**data)
    return JsonResponse({"msg":"created"})

def login_required(f):
    def wrapper(request):
        try:
            token = request.headers["authorization"].split(" ")[1]
            details = jwt.decode(token, "QWERTY", algorithms=["HS256"])
            print(details)
        except InvalidSignatureError:
            return JsonResponse({"err":"token error"}, status=401)
        except InvalidAlgorithmError:
            return JsonResponse({"err":"algorithm or secret key error"}, status=401)
        except DecodeError:
            return JsonResponse({"err":"invalid token error"}, status=401)
        except ExpiredSignatureError:
            return JsonResponse({"err":"token expired"}, status=401)
        return f(request)
    return wrapper



@api_view(["POST"])
def login(request):
    data = request.data 
    isUser = MyUser.objects.filter(email=data["email"]).first()
    if not isUser:
        return JsonResponse({"msg":"user not found"}, status=404)
    isPass = check_password(data['passwod'],isUser.passwod)
    if not isPass:
        return JsonResponse({"err":"invalid creds"}, status=400)
    token = jwt.encode({"id":isUser.id, "iat":datetime.utcnow(), "exp":datetime.utcnow() + timedelta(minutes=1)}, "QWERTY", algorithm="HS256")
    # print(token)
    return JsonResponse({"msg":"login success", "token":token})





@api_view(["GET"])
@login_required
def greet(request):
    return JsonResponse({"err":"okay"})