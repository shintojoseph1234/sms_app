from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
import json

def index(request):
    return render(request, 'login.html',{})

@login_required
def success(request):
    return render(request, 'success.html',{})

@csrf_exempt
def register(request):

    response_data = {}
    if request.POST:
        email       =   request.POST.get("email")
        password    =   request.POST.get("password")

        # if no user is present with the email then sign up
        if not User.objects.filter(username = email).exists():

            # create a user with the fields
            user = User.objects.create_user(
                                            username    = email,
                                            email       = email,
                                            password    = password,
                                            )
            # save the user in database
            user.save()
            response_data['status'] = 'success'
            return HttpResponse(json.dumps(response_data), content_type='application/json')

        else:
            response_data["status"] = 'fail'
            return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return render(request, 'register.html',{})


@csrf_exempt
def signin(request):


    response_data = {}
    if request.POST:

        try:
            # extract the data from the request
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(username=email, password=password)

            if user:
                login(request, user)
                response_data['status'] = "success"
            else:
                response_data['status'] = "fail"
        except:
            response_data['status'] = "fail"

    return HttpResponse(json.dumps(response_data), content_type='application/json')


def add(request):

    response_data = {}
    if request.POST:
        phone = request.POST.get("phone")

        # if no user is present with the email then sign up
        if User.objects.filter(username = request.user).exists():
            print (request.user.email)
            # print (type(request.user))

            p = PhoneModel( username   = str(request.user.email),
                            phone      = phone,
                            )
            # saving assigined data
            p.save()

            response_data['status'] = 'success'
            return HttpResponse(json.dumps(response_data), content_type='application/json')

        else:
            response_data["status"] = 'fail'
            return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return render(request, 'add.html',{})


@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



from sms.sendsms import sending_sms
@api_view(['POST'])
@method_decorator(csrf_exempt, name='dispatch')
def send_sms(request):

    try:
        data        = request.data['request']
        email       = data['email']
        password    = data['password']
        location    = data['location']

        phone_query_set = PhoneModel.objects.filter(username=str(email)).values('phone')

        phone_numbers = ''
        for each in phone_query_set:
            phone_numbers = phone_numbers +","+ each['phone']

        message = "Your friend "+email+" met with an emergency situation at location "+location
        messages, returns = sending_sms(message, phone_numbers)

        success = [{
                    "status": "success",
                    "data": {
                        "message": messages
                    }
                }]
    except:
        success = [{
                    "status": "Failure",
                    "data": {
                        "message": "Message sending failed"
                    }
                }]


    return Response(success, status=status.HTTP_200_OK)
