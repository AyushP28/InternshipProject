from django.shortcuts import render
from rest_framework import generics, permissions
from .models import CustomUser, Patient
from .serializers import CustomUserSerializer, PatientSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrSelf

# Create your views here.

class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": CustomUserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully. You can now Login to get your access and refresh token",
        })

class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return CustomUser.objects.all()
        else:
            return CustomUser.objects.filter(id=user.id)

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        hashed_password = make_password(password)
        serializer.save(password=hashed_password)

class CustomUserRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelf]

    @swagger_auto_schema(tags=["Custom Users"])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Custom Users"])
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Custom Users"])
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    @swagger_auto_schema(tags=["Patients"])
    def post(self, request, *args, **kwargs):
        
        return self.create(request, *args, **kwargs)

class PatientRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
    @swagger_auto_schema(tags=["Patients"])
    def get(self, request, *args, **kwargs):
        
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Patients"])
    def put(self, request, *args, **kwargs):
        
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Patients"])
    def delete(self, request, *args, **kwargs):
        
        return self.destroy(request, *args, **kwargs)



    

