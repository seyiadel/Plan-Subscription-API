from rest_framework import serializers
from distroapp.models import DistroUser
from django.contrib.auth import authenticate

class RegisterDistroAdminSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only = True)
    class Meta:
        model = DistroUser
        fields = ['email','first_name','last_name', 'password']

    def create(self, validated_data):
        distroadmin = DistroUser.objects.create_staffuser(**validated_data)
        return distroadmin


class LoginAdminSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email=attrs.get('email')
        password = attrs.get('password')
        if email and password:
            if DistroUser.objects.filter(email=email).exists():
                distroadmin = authenticate(request=self.context.get('request'),email=email, password=password)
            else:
                msg = {'detail': 'Email Address is not registered. Register.'}
                return serializers.ValidationError(msg)
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['distroadmin']=distroadmin
        return distroadmin