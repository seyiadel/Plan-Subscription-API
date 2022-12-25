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

class RegisterDistroUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DistroUser
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = DistroUser.objects.create_user(
                validated_data['email'],
                validated_data['first_name'],
                validated_data['last_name'],
                password =validated_data['password']
            )
            return user


