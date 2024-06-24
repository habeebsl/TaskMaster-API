from rest_framework import serializers
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ['email', 'username']

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data.get("email", None)
        user = User.objects.create_user(
            email=email,
            username=validated_data.get("username"),
            password=validated_data.get("password")
        )
        return user