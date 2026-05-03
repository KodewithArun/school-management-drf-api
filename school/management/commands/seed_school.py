from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from school.models import Subject, Class, Student, Teacher

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed database with test data for School models'

    def handle(self, *args, **kwargs):
        # Create Subjects
        math = Subject.objects.create(name='Mathematics')
        science = Subject.objects.create(name='Science')
        english = Subject.objects.create(name='English')

        # Create Classes
        class_a = Class.objects.create(name='Class A')
        class_b = Class.objects.create(name='Class B')
        class_a.subject.set([math, science])
        class_b.subject.set([english, science])

        # Create Users (username required by custom User model)
        student_user = User.objects.create_user(username='student1', email='student1@example.com', password='password123', role='student')
        teacher_user = User.objects.create_user(username='teacher1', email='teacher1@example.com', password='password123', role='teacher')

        # Create Student and Teacher
        student = Student.objects.create(user=student_user, classes=class_a)
        teacher = Teacher.objects.create(user=teacher_user)
        teacher.classes.set([class_a, class_b])
        teacher.class_teacher_of = class_a
        teacher.save()

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
