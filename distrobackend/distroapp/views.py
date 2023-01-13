from django.shortcuts import render
from rest_framework.views import APIView
from distroapp.seriailizers import PlanSerializer, RegisterDistroUserSerializer, LoginInDistroUserSerializer , DistroUserSerializer
from distroapp.models import Plan, DistroUser
from rest_framework.response import Response
from rest_framework import status, permissions , authentication
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginAPIView
from django.contrib.auth import login
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
import requests 
from distrobackend import settings


# Create your views here.
class IntroductionView(APIView):
    def get(self, request):
        return Response({"API_name":"Plan Subscription API",
                        "Description":"This API allows Payment to be made per plan",
                        "Swagger_documentation":"https://plan-subscription-api.onrender.com/swagger/",
                        "Developer_contact":{"Twitter":"https://twitter.com/seyiadel","Linkedin":"https://linkedin.com/in/oluwaloseyi-adeleye/"},
                        "API Github Repository":"https://github.com/seyiadel/Plan-Subscription-API/"})

class PlanView(APIView):
    """This is to get all plans created by the either the
    staff or superuser and are available to be purchased"""
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [TokenAuthentication,]

    def get(self, request):
        plan = Plan.objects.all()
        serializer=PlanSerializer(plan, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlanDetailView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [TokenAuthentication,]
    
    def get(self, request, id):
        plan= Plan.objects.get(id=id)
        serializer = PlanSerializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegisterDistroUserView(APIView):

    @swagger_auto_schema(request_body=RegisterDistroUserSerializer)
    def post(self, request):
        serializer= RegisterDistroUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

class LoginDistroUserView(KnoxLoginAPIView):
    permission_classes = (permissions.AllowAny,)
    """process the login details(email and password) to a token
    for authorization to be passed to as an header"""
    @swagger_auto_schema(request_body=LoginInDistroUserSerializer) #allows POST request defined seriailzer parametars to be passed in Swagger 
    def post (self, request):
        serializer = LoginInDistroUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)

class DistroUserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        serializer = DistroUserSerializer(self.request.user)
        return Response(serializer.data)


class ProcessDistroPlan(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication,]

    def post(self, request, plan_id):
        plan = Plan.objects.get(pk=plan_id)
        plan_price = plan.price * 100
        if self.request.user.status == True:
            return Response(data="You still have a valid plan, Can't make payment for another plan")
        url = "https://api.paystack.co/transaction/initialize"
        headers = {"authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        data= {"email": self.request.user.email,
                    "amount": plan_price,
        }
        response = requests.post(url, headers=headers, data=data)
        DistroUser.objects.filter(user_id=request.user.user_id).update(plan=plan.name)
    
        return Response(response.json())

class VerifyDistroPayment(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication,]

    def get(self, request, reference):
        url = "https://api.paystack.co/transaction/verify/{}".format(reference)
        headers = {"authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        response = requests.get(url, headers=headers)
        payload = response.json()
        if payload['data']['status'] =='success':
            DistroUser.objects.filter(user_id=request.user.user_id).update(status = True, 
                                                                            plan_start_date = payload['data']['paid_at'])
        return Response(payload)
        
        