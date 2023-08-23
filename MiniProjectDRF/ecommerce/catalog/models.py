from django.db import models


# Create your models here.
class KategoriProduk (models.Model):
    idKategori = models.AutoField(primary_key=True)
    namaKategori = models.CharField(max_length=100)

class Produk (models.Model):
    idProduk = models.AutoField(primary_key=True)
    namaProduk = models.CharField(max_length=100)
    hargaProduk = models.FloatField()
    kategori = models.ForeignKey(KategoriProduk, on_delete=models.CASCADE)