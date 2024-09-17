from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ais.models.teachers import Teachers

class Students(models.Model):
  # nim = models.PositiveBigIntegerField(unique=True, validators=[
  #   MinValueValidator(1), # NIM bernilai Positif
  #   MaxValueValidator(10**10-1) # NIM Maksimal 10 digit
  # ])
  nim = models.CharField(max_length=10, unique=True)
  name = models.CharField(max_length=255)
  email = models.EmailField(max_length=255, unique=True)
  phone_number = models.CharField(max_length=13, unique=True)
  year = models.IntegerField() # Tahun angkatan atau tahun masuk
  teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE) # Relasi ke tabel Teachers

  def __str__(self):
    return self.name