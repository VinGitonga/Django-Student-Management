from django.db import models
from django.contrib.auth.models import AbstractUser

gender_choices = (
    ('Male','Male'),
    ('Female','Female'),
    ('Others','Others')
)

religion_choices = (
    ('Muslim','Muslim'),
    ('Christian', 'Christian'),
    ('Hindu', 'Hindu'),
    ('Jain', 'Jain'),
    ('Others', 'Others')
)

session_choices = (
    ('Ist Semester','1st Semester'),
    ('2nd Semester', '2nd Semester'),
    ('3rd Semester', '3rd Semester')
)

section_choices = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C')
)


class Power(models.Model):
    read = models.BooleanField(default=True)
    create = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)

class User(AbstractUser):
    power = models.ForeignKey(Power, null=True, blank=True, on_delete=models.SET_NULL)
    pass

class Department(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=20)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    intake = models.IntegerField()
    created = models.DateField(auto_now_add=True)
    code = models.CharField(max_length=6)

    def __str__(self):
        return self.name


class Student(models.Model):
    admno = models.IntegerField()
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=50, choices=gender_choices)
    dob = models.DateField()
    dateofadmission = models.DateTimeField(auto_now_add=True)
    religion = models.CharField(max_length=50, choices=religion_choices)
    course = models.ForeignKey(Course, blank=True, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.SET_NULL)
    session = models.CharField(max_length=50, choices=session_choices)
    section = models.CharField(max_length=50, choices=section_choices)
    guardian = models.CharField(max_length=100)
    email = models.EmailField()
    phoneno = models.CharField(max_length=12)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.name} {self.course} {self.section}'

