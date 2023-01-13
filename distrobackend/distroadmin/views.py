from django.shortcuts import render
from distroadmin.serializers import RegisterDistroAdminSerializer, LoginAdminSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from distroapp.models import DistroUser, Plan
from distroapp.seriailizers import PlanSerializer
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
# Create your views here.

class RegisterDistroAdminView(APIView):
    permission_classes = ()
    @swagger_auto_schema(request_body=RegisterDistroAdminSerializer)
    def post(self, request):
        serializer= RegisterDistroAdminSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        admin=DistroUser.objects.filter(is_staff=True)
        serializer=RegisterDistroAdminSerializer(admin, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoginAdminView(KnoxLoginView):
    permission_classes=(permissions.AllowAny,)
    
    @swagger_auto_schema(request_body=LoginAdminSerializer)
    def post(self, request):
        serializer= LoginAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        distroadmin = serializer.validated_data
        if not distroadmin.is_staff == True:
            return Response(data='Only Staffs can login here!')
        login(request, distroadmin)
           
        return super().post(request, format=None)
           
        
class PlanAdminView(APIView):
    permission_classes = (permissions.IsAdminUser,)
    authentication_classes = [TokenAuthentication,]

    @swagger_auto_schema(request_body=PlanSerializer)
    def post(self, request):
        serializer=PlanSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        plan = Plan.objects.all()
        serializer=PlanSerializer(plan, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        plan=Plan.objects.all()
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlanDetailAdminView(APIView):
    permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

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
        