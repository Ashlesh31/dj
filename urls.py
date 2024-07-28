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
