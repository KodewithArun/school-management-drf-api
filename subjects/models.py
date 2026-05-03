from django.db import models
from accounts.models import BaseModel
from classes.models import Class
from teachers.models import Teacher

class Subject(BaseModel):
    name = models.CharField(max_length=100)
    classes = models.ManyToManyField(Class, related_name='subjects')
    teachers = models.ManyToManyField(Teacher, related_name='subjects_taught')

    def __str__(self):
        return self.name
