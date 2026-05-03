from django.db import models
from accounts.models import User, BaseModel

class Class(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Classes"

    def __str__(self):
        return self.name

class Section(BaseModel):
    name = models.CharField(max_length=100)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='sections')
    students = models.ManyToManyField('students.Student', related_name='class_sections')
    class_teacher = models.ForeignKey('teachers.Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='class_teacher_of')

    def __str__(self):
        return f"{self.class_id.name} - {self.name}"

class Timetable(BaseModel):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='timetable')
    day = models.CharField(max_length=20, choices=[
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE)
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.section} - {self.day} - {self.start_time}-{self.end_time} - {self.subject}"
