from django.shortcuts import render
from rest_framework.views import APIView
from distroapp.seriailizers import PlanSerializer
from distroapp.models import Plan
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class PlanView(APIView):
    def get(self, request):
        plan = Plan.objects.all()
        serializer=PlanSerializer(plan, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
