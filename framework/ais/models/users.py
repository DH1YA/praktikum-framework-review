from django.db import models

class Users(models.Model):
  STUDENT = 1
  TEACHER = 2
  ROLE_CHOICES = (
    (STUDENT, 'Student'),
    (TEACHER, 'Teacher'),
  )

  username = models.CharField(max_length=150, unique=True)
  password = models.CharField(max_length=128) # Panjang standar untuk password hash di Django
  role = models.IntegerField(choices=ROLE_CHOICES) # 1 = Student, 2 = Teacher

  def __str__(self):
    return self.username