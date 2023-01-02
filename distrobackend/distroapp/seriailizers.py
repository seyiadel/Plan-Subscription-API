from rest_framework import serializers
from distroapp.models import Plan , DistroUser
from django.contrib.auth import authenticate

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields= "__all__"

class DistroUserSerializer(serializers.ModelSerializer):
    plan_end_date=serializers.DateTimeField(source='plan_end_date_time', read_only=True)
    class Meta:
        model = DistroUser
        fields= "__all__"

    def validate(self, attrs):
        email = attrs.get('email')
        if email:
            if DistroUser.objects.filter(email=email).exists():
                msg = {'detail': 'Email Address is already associated with another user. Try a new one.', 'status':False}
                raise serializers.ValidationError(msg)
        return attrs

class RegisterDistroUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=14, write_only=True)
    class Meta:
        model = DistroUser
        fields = ['first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = DistroUser.objects.create_user(**validated_data)
        return user

class LoginInDistroUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=14, write_only=True)
 
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            if DistroUser.objects.filter(email=email).exists():
                user = authenticate(request=self.context.get('request'), email=email, password=password)

            else:
                msg = {'detail': 'Email Address is not registered. Register.'}
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs