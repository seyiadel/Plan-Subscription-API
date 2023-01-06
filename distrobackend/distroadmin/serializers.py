from rest_framework import serializers
from distroapp.models import DistroUser


class RegisterDistroAdminSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only = True)
    class Meta:
        model = DistroUser
        fields = ['email','first_name','last_name', 'password']

    def create(self, validated_data):
        distroadmin = DistroUser.objects.create_staffuser(**validated_data)
        return distroadmin