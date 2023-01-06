from django.shortcuts import render
from distroadmin.serializers import RegisterDistroAdminSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from distroapp.models import DistroUser
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