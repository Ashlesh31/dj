
// model
from django.db import models
class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.name   
    

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)


class Meta:
    unique_together = ('student', 'course')
    def __str__(self):
        return f"{self.student} enrolled in {self.course}"


class Project(models.Model): 
        student = models.OneToOneField(Student, on_delete=models.CASCADE) 
        topic = models.CharField(max_length=200) 
        languages_used = models.CharField(max_length=200) 
        duration = models.PositiveIntegerField(help_text="Duration in weeks") 
        def __str__(self): 
            return f"{self.topic} by {self.student}"













// forms
from django import forms
from .models import Student, Course, Enrollment, Project

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email']
    
class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['student', 'topic', 'language_used', 'duration']















//urls
from program5  import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register_student/', views.register_student, name='register_student'),
    path('enroll_student/<int:student_id>/', views.enroll_student, name='enroll_student'),
    path('enrollment_list/', views.enrollment_list, name='enrollment_list'),
    path('add_project/', views.add_project, name='add_project'), 
    path('project_list/', views.project_list, name='project_list'),
    path('students/', views.StudentListView.as_view(), name='student_list'), 
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('export_students_csv/', views.export_students_csv, name='export_students_csv'), 
    path('export_students_pdf/', views.export_students_pdf, name='export_students_pdf'),
]














//admin
from django.contrib import admin
from .models import Student, Course, Enrollment, Project
# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name','email')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date_enrolled')
    search_fields = ('student.first_name', 'student.last_name', 'course.name')
    list_filter = ['date_enrolled']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('student', 'topic', 'language_used', 'duration')
    search_fields = ('student__first_name', 'student__last_name', 'topic')














// views
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


//templates

<!DOCTYPE html>
<html lang="en">
<head>
    <title>Register Student</title>
    {% load static %}
    <link rel="stylesheet" type="text/css" href="{% static 'program5/styles.css' %}">
</head>
<body>
    <h2>Student Registration</h2>
    <form method = 'post'>
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Register</button>
    </form>
</body>
</html>


<!DOCTYPE html>
<html lang="en">
<head>
    <title>Enroll student</title>
    {% load static %}
    <link rel="stylesheet" type="text/css" href="{% static 'program5/styles.css' %}">
</head>
<body>
    <h2>Enroll Student</h2>
    <form method = 'post'>
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Enroll</button>
    </form>
</body>
</html>


<!DOCTYPE html>
<html lang="en">
<head>
    <title>Enrollment List</title>
    {% load static %}
    <link rel="stylesheet" type="text/css" href="{% static 'program5/styles.css' %}">
</head>
<body>
    <h2>Enrollment student</h2>
    <ul>
        {% for enrollment in enrollments %}
            <li>{{ enrollment.student.first_name }} enrolled in {{ enrollment.course.name }} on {{ enrollment.date_enrolled }}</li>
        {% endfor %}
    </ul>
</body>
</html>


<!DOCTYPE html>
<html lang="en">
<head>
    <title>Register Student</title>
    {% load static %}
    <link rel="stylesheet" type="text/css" href="{% static 'program5/styles.css' %}">
</head>
<body>
    <h2>Add Project</h2>
    <form method = 'post'>
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">save</button>
    </form>
</body>
</html>


<!DOCTYPE html>
<html lang="en">
<head>
    <title>Projects List</title>
    {% load static %}
    <link rel="stylesheet" type="text/css" href="{% static 'program5/styles.css' %}">
</head>
<body>
    <h2>Projects student</h2>
    <ul>
        {% for project in projects %}
        <li>{{ project.student.first_name }} {{ project.student.last_name }}: {{ project.topic }} - {{ project.languages_used }} ({{ project.duration }} weeks)</li>
        {% endfor %}
    </ul>
</body>
</html>


<!DOCTYPE html>
<html>
<head>
    <title>Student List</title>
    {% load static %}
    <link rel="stylesheet" type="text/css" href="{% static 'program5/styles.css' %}">
</head>
<body>
    <div class="container">
        <h1>Student List</h1>
        <a href="{% url 'export_students_csv' %}">Export as CSV</a> |
        <a href="{% url 'export_students_pdf' %}">Export as PDF</a>
        <ul>
            {% for student in students %}
            <li><a href="{% url 'student_detail' student.pk %}">{{ student.first_name }} {{ student.last_name }}</a></li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>


<!DOCTYPE html> 
<html> 
<head> 
    <title>Student Detail</title> 
    {% load static %} 
    <link rel="stylesheet" type="text/css" href="{% static 'program5/styles.css' %}"> 
</head> 
<body> 
    <div class="container"> 
        <h1>{{ student.first_name }} {{ student.last_name }}</h1> 
        <p><strong>Email:</strong> {{ student.email }}</p> 
        <h2>Enrolled Courses</h2> 
        <ul> 
            {% for enrollment in student.enrollment_set.all %} 
                <li>{{ enrollment.course.name }} - {{ enrollment.date_enrolled }}</li> 
            {% endfor %} 
        </ul> 
        <h2>Project</h2> 
        {% if student.project %} 
            <p><strong>Topic:</strong> {{ student.project.topic }}</p> 
            <p><strong>Languages Used:</strong> {{ student.project.languages_used }}</p> 
            <p><strong>Duration:</strong> {{ student.project.duration }} 
weeks</p> 
        {% else %} 
            <p>No project assigned.</p> 
        {% endif %} 
    </div> 
</body> 
</html> 
