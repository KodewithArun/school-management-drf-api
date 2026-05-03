from django.db import models
from django.conf import settings

user = settings.AUTH_USER_MODEL

class Subject(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ManyToManyField(Subject,related_name='classes')
    
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    classes = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    
    def __str__(self):
        return self.user.email
    
class Teacher(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    classes = models.ManyToManyField(Class, related_name='teachers')
    class_teacher_of=models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True, related_name='class_teacher')
    
    def __str__(self):
        return self.user.email
    
    
    

