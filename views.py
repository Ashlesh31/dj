from io import BytesIO
from django.shortcuts import render, redirect 
from django.views.generic import ListView, DetailView 
from .models import Project, Student, Course, Enrollment 
from .forms import ProjectForm, StudentForm, EnrollmentForm
import csv 
from django.http import HttpResponse 
from reportlab.lib.pagesizes import letter 
from reportlab.pdfgen import canvas
from django.http import JsonResponse 

def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect('enroll_student', student_id=student.id)
    else:
        form = StudentForm()
    return render(request, 'program5/register_student.html', {'form': form})

def enroll_student(request, student_id):
    student = Student.objects.get(id=student_id)
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = student
            enrollment.save()
            return redirect('enrollment_list')
    else:
        form = EnrollmentForm(initial={'student': student})
    return render(request, 'program5/enroll_student.html', {'form': form, 'student': student})

def enrollment_list(request):
    enrollments = Enrollment.objects.all()
    return render(request, 'program5/enrollment_list.html', {'enrollments': enrollments})

def add_project(request): 
    if request.method == 'POST': 
        form = ProjectForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect('project_list') 
    else: 
        form = ProjectForm() 
    return render(request, 'program5/add_project.html', {'form': form})

def project_list(request): 
    projects = Project.objects.all() 
    return render(request, 'program5/project_list.html', {'projects': projects})


class StudentListView(ListView): 
    model = Student 
    template_name = 'program5/student_list.html' 
    context_object_name = 'students' 


class StudentDetailView(DetailView): 
    model = Student 
    template_name = 'program5/student_detail.html' 
    context_object_name = 'student' 


def export_students_csv(request): 
    response = HttpResponse(content_type='text/csv') 
    response['Content-Disposition'] = 'attachment; filename="students.csv"' 
    writer = csv.writer(response) 
    writer.writerow(['First Name', 'Last Name', 'Email']) 
    students = Student.objects.all() 
    for student in students: 
        writer.writerow([student.first_name, student.last_name, student.email]) 
    return response 

# PDF generation view 
def export_students_pdf(request): 
    response = HttpResponse(content_type='application/pdf') 
    response['Content-Disposition'] = 'attachment; filename="students.pdf"' 
 
    buffer = BytesIO() 
    p = canvas.Canvas(buffer, pagesize=letter) 
 
    p.drawString(100, 750, "Students List") 
    p.drawString(100, 730, "=================") 
 
    students = Student.objects.all() 
    y = 710 
    for student in students: 
        p.drawString(100, y, f"{student.first_name} {student.last_name} - {student.email}") 
        y -= 20 
 
    p.showPage() 
    p.save() 
 
    buffer.seek(0) 
    return HttpResponse(buffer, content_type='application/pdf')
