from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentsForm
from .models import Students
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .decorators import group_required
from rest_framework import viewsets
from .serializers import StudentsSerializer
import requests

# Create your views here.
def homepage(request):
    return render(request, 'homepage/index.html')

def about(request):
    return render(request, 'homepage/about.html')

# READ Mahasiswa
def student_index(request):
    query = request.GET.get('q')
    
    # Fetch students based on the search query
    if query:
        response = requests.get(f'http://127.0.0.1:8000/api/students/?search={query}')
    else:
        response = requests.get('http://127.0.0.1:8000/api/students/')
    
    # Check if the request was successful
    if response.status_code == 200:
        students = response.json()  # Get student data in JSON format
    else:
        students = []  # If failed, prepare an empty list

    # Render the index template with the student data and query
    return render(request, 'student/index.html', {'students': students, 'query': query})

# CREATE Mahasiswa
def student_create(request):
    if request.method == 'POST':
        form_data = {
            'name': request.POST.get('name'),
            'nim': request.POST.get('nim'),
            'email': request.POST.get('email'),
            'phone_number': request.POST.get('phone_number'),
            'year': request.POST.get('year'),  # Ensure year is taken from the form
            'teacher': request.POST.get('teacher'),  # Teacher ID from dropdown
        }

        # Sending POST request to the API
        response = requests.post('http://127.0.0.1:8000/api/students/', data=form_data)

        if response.status_code == 201:  # Created
            messages.success(request, 'Mahasiswa berhasil dibuat!')  # Success message
            return redirect('student_index')  # Redirect to student index page
        else:
            messages.error(request, 'Gagal membuat mahasiswa: ' + response.text)  # Error message if failed
    else:
        form_data = {}

    return render(request, 'student/create.html', {'form': StudentsForm()})  # Send form to template

# UPDATE Mahasiswa
def student_update(request, student_id):
    # Fetch the existing student data from the API
    response = requests.get(f'http://127.0.0.1:8000/api/students/{student_id}/')

    if response.status_code == 200:
        student = response.json()  # Get student data in JSON format
    else:
        return HttpResponseForbidden("Data mahasiswa tidak ditemukan.")  # Handle not found

    if request.method == 'POST':
        form_data = {
            'name': request.POST.get('name'),
            'nim': request.POST.get('nim'),
            'email': request.POST.get('email'),
            'phone_number': request.POST.get('phone_number'),
            'year': request.POST.get('year'),  # Get year from the form
            'teacher': request.POST.get('teacher'),  # Teacher ID from dropdown
        }

        # Send PUT request to the API to update the student
        response = requests.put(f'http://127.0.0.1:8000/api/students/{student_id}/', data=form_data)

        if response.status_code == 200:  # OK
            messages.success(request, 'Data mahasiswa berhasil diubah!')  # Success message
            return redirect('student_index')  # Redirect to student index page
        else:
            messages.error(request, 'Gagal mengubah mahasiswa: ' + response.text)  # Error message if failed

    # Render the update form with existing student data
    return render(request, 'student/update.html', {'form': StudentsForm(initial=student), 'student': student})

# DELETE Mahasiswa
def student_delete(request, student_id):
    if request.method == 'POST':  # Only accept POST for deletion
        response = requests.delete(f'http://127.0.0.1:8000/api/students/{student_id}/')

        if response.status_code == 204:  # No Content, means successful deletion
            messages.success(request, 'Data mahasiswa berhasil dihapus.')
            return JsonResponse({'success': True})
        else:
            messages.error(request, 'Gagal menghapus mahasiswa: ' + response.text)
            return JsonResponse({'success': False})
    else:
        return HttpResponseForbidden("Metode tidak diizinkan.")  # Forbidden for other methods

# SEARCH
def student_index(request):
    query = request.GET.get('q')
    if query:
        students = Students.objects.filter(
            Q(name__icontains=query) |
            Q(nim__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query)
        )
    else:
        students = Students.objects.all()
    
    return render(request, 'student/index.html', {'students': students, 'query': query})

# * DASHBOARD
@login_required
def dashboard(request):
    user = request.user
    if user.groups.filter(name='Admin').exists():
        return redirect('dashboard_admin')
    elif user.groups.filter(name='Student').exists():
        return redirect('dashboard_student')
    elif user.groups.filter(name='Teacher').exists():
        return redirect('dashboard_teacher')
    return HttpResponseForbidden("You do not have permission to access this page.")

@login_required
@group_required('Admin')
def dashboard_admin(request):
    return render(request, 'dashboard/admin.html')

@login_required
@group_required('Student')
def dashboard_student(request):
    return render(request, 'dashboard/student.html')

@login_required
@group_required('Teacher')
def dashboard_teacher(request):
    return render(request, 'dashboard/teacher.html')

# API
class StudentsViewSet(viewsets.ModelViewSet):
    """
    API endpoint yang memungkinkan operasi CRUD untuk model Students.
    """
    queryset = Students.objects.all() # Mengambil semua data mahasiswadari database
    serializer_class = StudentsSerializer # Menggunakan serializer yang sudah kita buat