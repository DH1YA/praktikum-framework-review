from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

class Teachers(models.Model):
    nip = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)

def __str__(self):
    return self.name

# Signal untuk membuat User ketika Teacher dibuat
@receiver(post_save, sender=Teachers)
def create_user_for_teacher(sender, instance, created, **kwargs):
    if created:
        # Membuat User yang sesuai
        user = User.objects.create_user(
            username=instance.nip,  # Menggunakan NIP sebagai username
            email=instance.email,
            password=instance.nip  # Atur default password atau ganti sesuai kebutuhan
        )
        # Menambahkan user ke grup 'Teacher'
        teacher_group, _ = Group.objects.get_or_create(name='Teacher')
        user.groups.add(teacher_group)

# # Signal untuk membuat User ketika Student dibuat
# @receiver(post_save, sender=Students)
# def create_user_for_student(sender, instance, created, **kwargs):
#     if created:
#         # Membuat User yang sesuai
#         user = User.objects.create_user(
#             username=instance.nim,  # Menggunakan NIM sebagai username
#             email=instance.email,
#             password=instance.nim  # Atur default password atau ganti sesuai kebutuhan
#         )
#         # Menambahkan user ke grup 'Student'
#         student_group, _ = Group.objects.get_or_create(name='Student')
#         user.groups.add(student_group)