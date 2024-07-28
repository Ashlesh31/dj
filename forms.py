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

    
