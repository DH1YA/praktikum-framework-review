from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from ais.models.teachers import Teachers

class Students(models.Model):
    nim = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)
    year = models.IntegerField() # Tahun angkatan atau tahun masuk
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE) # Relasi ke tabel Teachers

def __str__(self):
    return self.name

# Signal untuk membuat User ketika Student dibuat
@receiver(post_save, sender=Students)
def create_user_for_student(sender, instance, created, **kwargs):
    if created:
        # Membuat User yang sesuai
        user = User.objects.create_user(
            username=instance.nim,  # Menggunakan NIM sebagai username
            email=instance.email,
            password=instance.nim  # Atur default password atau ganti sesuai kebutuhan
        )
        # Menambahkan user ke grup 'Student'
        # student_group, _ = Group.objects.get_or_create(name='Student')
        student_group, created = Group.objects.get_or_create(name='Student')
        user.groups.add(student_group)