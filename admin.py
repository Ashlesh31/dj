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

