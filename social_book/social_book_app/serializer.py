from rest_framework import serializers
from .models import UploadedFile
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'title', 'description', 'visibility', 'cost', 'year_published', 'file']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        print(f"Authenticating user: {username}")

        user = authenticate(username=username, password=password)

        if not user:
            print("Authentication failed")
            raise serializers.ValidationError('Invalid username or password')

        print("Authentication successful")

        token, created = Token.objects.get_or_create(user=user)

        return {
            'username': user.username,
            'token': token.key
        }
    
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['file', 'uploaded_at']