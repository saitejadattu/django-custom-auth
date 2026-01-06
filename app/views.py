from django.shortcuts import render
from .models import MyUser
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
# Create your views here.
from rest_framework.decorators import api_view
import jwt
# from jwt import inva
from bcrypt import hashpw, checkpw

@api_view(["POST"])
def register(request):
    data = request.data 
    data["passwod"] = make_password(data["passwod"])
    MyUser.objects.create(**data)
    return JsonResponse({"msg":"created"})

def login_required(f):
    def wrapper(request):
        # try:
        token = request.headers["authorization"].split(" ")[1]
        details = jwt.decode(token, "QWERTY", algorithms=["HS256"])
        print(details)
        # except:
        #     return JsonResponse({"err":"jwt error"}, status=401)
        # print()
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
    token = jwt.encode({"id":isUser.id}, "QWERTY", algorithm="HS256")
    # print(token)
    return JsonResponse({"msg":"login success", "token":token})





@api_view(["GET"])
@login_required
def greet(request):
    return JsonResponse({"err":"invaklid"})