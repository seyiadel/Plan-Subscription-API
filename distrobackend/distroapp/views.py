from django.shortcuts import render
from rest_framework.views import APIView
from distroapp.seriailizers import PlanSerializer, RegisterDistroUserSerializer
from distroapp.models import Plan
from rest_framework.response import Response
from rest_framework import status
from knox.models import AuthToken

# Create your views here.
class PlanView(APIView):
    def get(self, request):
        plan = Plan.objects.all()
        serializer=PlanSerializer(plan, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    
    def get(self, request, id):
        plan= Plan.objects.get(id=id)
        serializer = PlanSerializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    def post(self, request):
        serializer= RegisterDistroUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            return Response({
                'user':serializer.data,
                'token':AuthToken.objects.create(user)[1],
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)