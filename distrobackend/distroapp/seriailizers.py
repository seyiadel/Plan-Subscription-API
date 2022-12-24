from rest_framework import serializers
from distroapp.models import Plan , DistroUser

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields= "__all__"

class DistroUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistroUser
        fields= "__all__"