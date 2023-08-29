from django.contrib.auth.models import User
from .models import KategoriProduk,Produk
from rest_framework import serializers
from rest_framework.response import Response

class KategoriSerializers (serializers.ModelSerializer):
    class Meta :
        model = KategoriProduk
        fields = ['idKategori','namaKategori']

class ProdukSerializers (serializers.ModelSerializer):
    class Meta :
        model = Produk
        fields = ['idProduk','namaProduk', 'hargaProduk', 'kategori']


class userRegisSerializers (serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password' : {'write_only' : True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return{
            "msg" : "User baru telah ditambahkan",
            "username" : user.username,
            "email" : user.email,
        }

class userSerializers (serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ['id', 'username', 'email']

class LoginSerializers (serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)