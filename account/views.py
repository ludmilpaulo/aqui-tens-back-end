import json
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from shop.permissions import *

from rest_framework import status, generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.parsers import *
from rest_framework import serializers


from shop.models import *
from .serializers import *




from django.core.exceptions import ObjectDoesNotExist

from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth import get_user_model
User = get_user_model()



AccessToken = Token

class DriverSignupView(generics.GenericAPIView):
    serializer_class=DriverSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            'user_id':user.pk,
            "message":"Conta criada com sucesso",
            'username':user.username,
            "status":"201"
        })




class CustomerSignupView(generics.CreateAPIView):
    serializer_class = CustomerSignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Call save method to create user and customer
        user = serializer.save()

        # Construct response data
        data = {
            "user_id": user.pk,
            "message": "Conta criada com sucesso",
            "username": user.username,
            "status": status.HTTP_201_CREATED,
            "is_customer": user.is_customer
        }

        return Response(data, status=status.HTTP_201_CREATED)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token, created=Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'username':user.username,
            'message':"Login com sucesso",
            'is_customer':user.is_customer
        })


class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


class CustomerOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsCustomerUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user

class DriverOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsDriverUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user

####################################################
# CUSTOMERS
####################################################

@api_view(["POST"])
@parser_classes([JSONParser, MultiPartParser, FormParser, FileUploadParser])
def customer_update_profile(request, format=None):
    data = request.data
    access = Token.objects.get(key=data['access_token']).user

    customer = Customer.objects.get(user=access)

    # Set location string => database
    customer.avatar = request.FILES.get('avatar')
    #driver.avatar = data['avatar']
    customer.phone = data["phone"]
    customer.address = data["address"]
    customer.save()

    customer_user = User.objects.get(username=access)
    customer_user.first_name = data["first_name"]
    customer_user.last_name = data["last_name"]
    customer_user.save()

    return JsonResponse({"status": "Os Seus Dados enviados com sucesso"})


class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f'http://127.0.0.1:8000/reset-password/{uid}/{token}/'

            send_mail(
                'Reset your password',
                f'Click the following link to reset your password: {reset_link}',
                'from@example.com',
                [email],
                fail_silently=False,
            )

            return Response({'message': 'Password reset link sent successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
