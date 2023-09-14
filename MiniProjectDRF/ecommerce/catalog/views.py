from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics,viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly
from .models import KategoriProduk,Produk
from .serializers import KategoriSerializers, ProdukSerializers,userSerializers,userRegisSerializers,LoginSerializers
from rest_framework_simplejwt.tokens import RefreshToken



class KategoriViews (generics.ListCreateAPIView):
    queryset = KategoriProduk.objects.all()
    serializer_class = KategoriSerializers
    permission_classes = [IsAuthenticated]

class ProdukViews(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Produk.objects.all()
        harga = self.request.query_params.get('price', None)
        limit = self.request.query_params.get('limit', None)
        nama = self.request.query_params.get('name', None)
        offset = self.request.query_params.get('offset', None)
        kategori = self.request.query_params.get('categories', None)

        if nama is not None :
            queryset = queryset.filter(namaProduk = nama)

        if harga is not None :
            queryset = queryset.filter(hargaProduk = harga)

        if kategori is not None :
            queryset = queryset.filter(kategori = kategori)
        
        if limit is not None :
            if offset is None :
                queryset = queryset[:int(limit)] 
            else :
                queryset = queryset[int(offset):int(limit)]      
        
        jumlahData = queryset.count()
        
        return (queryset,jumlahData)
    
    
    def list(self, request):
        queryset = self.get_queryset()[0]
        count = self.get_queryset()[1]

        if count == 0 :
            return Response({
                "message" : "data tidak ditemukan"
            })
        
        serializer = ProdukSerializers(queryset, many=True)
        data = serializer.data

        response = {
            "messege" : "berikut data yang anda butuhkan :",
            "Jumlah Data" : count,
            "result" : data,
        }

        return Response(response, status=status.HTTP_200_OK)
    
    
    def create(self, request, *args, **kwargs):
        serializer = ProdukSerializers(data= request.data)

        if serializer.is_valid(raise_exception= True) :
            serializer.save()
            response = {
                "message" : "Produk baru berhasil ditambahkan!",
                "data" : serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def retrieve(self, request, pk = None):
        queryset = self.get_queryset()[0]
        produk = get_object_or_404(queryset, pk=pk)
        serializer = ProdukSerializers(produk)
        response = {
            "message" : "detail produk berhasil didapatkan",
            "data" : serializer.data
        }
        return Response(response)
    
    def update(self, request, pk = None):

        queryset = self.get_queryset()[0]
        produk = get_object_or_404(queryset, pk=pk)
        serializer = ProdukSerializers(produk, data = request.data)
        if serializer.is_valid():
            serializer.save()

        return Response({
            "message" : "data produk berhasil diupdate"
        })
          

class userRegisterViews (generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = userRegisSerializers
    

class userListViews (generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()
    serializer_class = userSerializers
    permission_classes = [IsAuthenticated]

class userLoginViews(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username)

        for user_check in user:
            if user_check.check_password(password) :
                refresh = RefreshToken.for_user(user_check) 
                return Response({
                    'message' : 'anda berhasil login',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
                
            else:
                return Response({
                    "message" : "password yang anda masukan salah"
                })
        
        return Response({
                'message' : 'user tidak ditemukan'
            })


        
            








        




