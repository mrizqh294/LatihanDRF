from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics,viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly
from .models import KategoriProduk,Produk
from .serializers import KategoriSerializers, ProdukSerializers,userSerializers,userRegisSerializers,LoginSerializers
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class KategoriViews (generics.ListCreateAPIView):
    queryset = KategoriProduk.objects.all()
    serializer_class = KategoriSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProdukViews(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Produk.objects.all()
        harga = self.request.query_params.get('harga', None)
        limit = self.request.query_params.get('limit', None)

        if harga is not None :
            queryset = queryset.filter(hargaProduk = harga)
        
        if limit is not None :
            queryset = queryset[int(limit)]
        
        jumlahData = queryset.count()
        
        return (queryset,jumlahData)
    
    def list(self, request):
        queryset = self.get_queryset()[0]
        count = self.get_queryset()[1]
        serializer = ProdukSerializers(queryset, many=True)
        data = serializer.data

        return Response({
            "messege" : "berikut data yang anda butuhkan :",
            "Jumlah Data" : count,
            "result" : data,
        })
    
        

class userRegisterViews (generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = userRegisSerializers
    

class userListViews (generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = userSerializers
    permission_classes = [IsAuthenticated]

class userLoginViews(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        if user is None :
            return Response({
                "message" : "user tidak ditemukan"
            })
        
        if not user.check_password(password) :
            return Response({
                "message" : "password yang anda masukan salah"
            })
       
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    
        

        
            








        




