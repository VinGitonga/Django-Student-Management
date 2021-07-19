from django import forms
from django.contrib.auth.forms import UserCreationForm,UsernameField
from django.db import transaction

# from django.forms.utils import ValidationError
from .models import User, Department, Course, Student


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        field_classes = {"username": UsernameField}

    @transaction.atomic
    def save(self, commit=False):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

        return user

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', ]

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ['created']
        fields = '__all__'

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['admno', 'name', 'gender', 'dob', 'course', 'religion', 'session',\
            'section','guardian','email','phoneno','address','city','postal_code','country']


class SearchForm(forms.ModelForm):
    export_to_csv = forms.BooleanField(required=False)
    class Meta:
        model = Course
        fields = ['name', ]
