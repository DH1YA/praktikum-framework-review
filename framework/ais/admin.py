from django.contrib import admin
from django.contrib.auth.hashers import make_password # Untuk hashing password
# Model untuk Teachers
from .models.teachers import Teachers
# Model untuk Students
from .models.students import Students
# Model untuk Users
from .models.users import Users

class TeacherAdmin(admin.ModelAdmin):
  list_display = ('nip', 'name', 'email', 'phone_number')

  def save_model(self, request, obj, form, change):
    # Simpan Teacher terlebih dahulu
    super().save_model(request, obj, form, change)

    # Cek apakah user dengan email guru sudah ada
    user, created = Users.objects.get_or_create(username=obj.nip, defaults={ # Pastikan ini model Users kustom
    'password': make_password('default_password'), # Menggunakan hashing password
    'role': Users.TEACHER # Pastikan Anda memiliki field role di model Users
    })

    if not created:
      # Jika user sudah ada, perbarui role (untuk berjaga-jaga)
      user.role = Users.TEACHER
      user.save()

# Daftarkan Teachers dengan custom TeacherAdmin
admin.site.register(Teachers, TeacherAdmin)
# Daftarkan Model Students dan Users
admin.site.register(Students)
admin.site.register(Users)