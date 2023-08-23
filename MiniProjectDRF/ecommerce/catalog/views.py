from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly
from .models import KategoriProduk,Produk
from .serializers import KategoriSerializers, ProdukSerializers,userSerializers,userRegisSerializers,LoginSerializers

# Create your views here.

class KategoriViews (generics.ListCreateAPIView):
    queryset = KategoriProduk.objects.all()
    serializer_class = KategoriSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProdukListViews (generics.ListCreateAPIView):
    queryset = Produk.objects.all()
    serializer_class = ProdukSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]

class userRegisterViews (generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = userRegisSerializers
    permission_classes = [AllowAny]

class userListViews (generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = userSerializers
    permission_classes = [IsAuthenticated]

class userLoginViews(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        serializer = LoginSerializers(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({'message': 'Anda Berhasil Login'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'login gagal'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




