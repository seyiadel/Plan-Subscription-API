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
class PlanView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication,]

    def get(self, request):
        plan = Plan.objects.all()
        serializer=PlanSerializer(plan, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PlanSerializer)
    def post(self, request):
        serializer=PlanSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        plan=Plan.objects.all()
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class PlanDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication,]
    
    def get(self, request, id):
        plan= Plan.objects.get(id=id)
        serializer = PlanSerializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PlanSerializer)
    def put(self, request, id):
        plan= Plan.objects.get(id=id)
        serializer = PlanSerializer(instance=plan, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self,request, id):
        plan = Plan.objects.get(id=id)
        plan.delete()
        return Response(data="Plan Deleted", status=status.HTTP_204_NO_CONTENT)


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

    @swagger_auto_schema(request_body=LoginInDistroUserSerializer)
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
        if self.request.user.status == True:
            return Response(data="You still have a valid plan, Can't make payment for another plan")
        url = "https://api.paystack.co/transaction/initialize"
        headers = {"authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        data= {"email": self.request.user.email,
                    "amount": plan.price,
        }
        response = requests.post(url, headers=headers, data=data)
        DistroUser.objects.filter(user_id=request.user.user_id).update(plan=plan)
    
        return Response(response.json())

class VerifyDistroPayment(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication,]

    def get(self, request, reference):
        url = "https://api.paystack.co/transaction/verify/{}".format(reference)
        headers = {"authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        response = requests.get(url, headers=headers)
        payload=response.json()
        if payload['data']['status']=='success':
            DistroUser.objects.filter(user_id=request.user.user_id).update(status=True, plan_start_date=payload['data']['paid_at'])
        return Response(payload)
        
