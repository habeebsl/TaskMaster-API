from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.authtoken.views import Token
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from .serializers import RegisterSerializer, UserSerializer

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user_view(request):
    request_data = request.data
    serializer = RegisterSerializer(data=request_data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(request_data).data,
            "token": token.key
        })
    