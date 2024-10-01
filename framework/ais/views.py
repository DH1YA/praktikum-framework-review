from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Students
from .forms import StudentsForm

# Create your views here.
def homepage(request):
  return render(request, 'homepage/index.html')

def about(request):
  return render(request, 'homepage/about.html')

# READ Mahasiswa
def student_index(request):
  students = Students.objects.all()
  return render(request, 'student/index.html', {'students': students})

# CREATE Mahasiswa
def student_create(request):
  if request.method == 'POST':
    form = StudentsForm(request.POST)
    if form.is_valid():
      form.save() # Simpan data mahasiswa ke database
      messages.success(request, 'Mahasiswa berhasil dibuat!') # Pesan sukses
      return redirect('student_index') # Redirect ke halaman index mahasiswa
  else:
    form = StudentsForm()
    
  return render(request, 'student/create.html', {'form': form})