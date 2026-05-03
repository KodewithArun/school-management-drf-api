from django.db import models
from accounts.models import User, BaseModel
from classes.models import Class

class Student(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', limit_choices_to={'role': 'student'})
    classes = models.ManyToManyField(Class, related_name='students_in_class')

    def __str__(self):
        return self.user.email
