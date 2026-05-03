from django.db import models
from accounts.models import User, BaseModel
from classes.models import Class

class Teacher(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile', limit_choices_to={'role': 'teacher'})
    classes = models.ManyToManyField(Class, related_name='teachers_in_class')
    
    def __str__(self):
        return self.user.email
