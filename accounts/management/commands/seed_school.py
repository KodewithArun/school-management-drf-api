import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import User
from classes.models import Class, Section, Timetable
from students.models import Student
from teachers.models import Teacher
from subjects.models import Subject

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with initial school data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Cleaning up old data...')
        User.objects.all().delete()
        Class.objects.all().delete()
        Subject.objects.all().delete()
        
        self.stdout.write('Seeding new data...')

        # 1. Create Principal
        principal_user, created = User.objects.get_or_create(
            email='principal@gmail.com',
            username='principal',
            defaults={'role': 'principal'}
        )
        principal_user.set_password('password123')
        principal_user.save()
        self.stdout.write(f'Principal created: {principal_user.email}')

        # 2. Create Classes
        grades = ['Grade 10', 'Grade 11', 'Grade 12']
        class_objects = []
        for g in grades:
            obj, created = Class.objects.get_or_create(name=g)
            class_objects.append(obj)
        self.stdout.write(f'{len(class_objects)} classes created.')

        # 3. Create Teachers
        teachers_data = [
            ('ram.sharma@gmail.com', 'Ram Prasad', 'Sharma'),
            ('sita.thapa@gmail.com', 'Sita Kumari', 'Thapa'),
            ('binod.shrestha@gmail.com', 'Binod', 'Shrestha'),
        ]
        teacher_profiles = []
        for email, first, last in teachers_data:
            user, created = User.objects.get_or_create(
                email=email,
                username=email.split('@')[0],
                defaults={'role': 'teacher', 'first_name': first, 'last_name': last}
            )
            user.set_password('password123')
            user.save()
            
            profile, created = Teacher.objects.get_or_create(user=user)
            # Assign to some classes
            profile.classes.set(random.sample(class_objects, k=2))
            teacher_profiles.append(profile)
        self.stdout.write(f'{len(teacher_profiles)} teachers created.')

        # 4. Create Subjects
        subject_names = ['Mathematics', 'Science', 'Nepali', 'Social Studies', 'English', 'Computer Science']
        subjects = []
        for name in subject_names:
            obj, created = Subject.objects.get_or_create(name=name)
            obj.classes.set(class_objects)
            obj.teachers.set(random.sample(teacher_profiles, k=2))
            subjects.append(obj)
        self.stdout.write(f'{len(subjects)} subjects created.')

        # 5. Create Sections
        sections = []
        for cls in class_objects:
            for sec_name in ['A', 'B']:
                sec, created = Section.objects.get_or_create(
                    name=sec_name,
                    class_id=cls,
                    defaults={'class_teacher': random.choice(teacher_profiles)}
                )
                sections.append(sec)
        self.stdout.write(f'{len(sections)} sections created.')

        # 6. Create Students
        student_names = [
            ('Aryan', 'Thapa'), ('Smriti', 'Gurung'), ('Rohan', 'Shrestha'),
            ('Anjali', 'Tamang'), ('Bibek', 'Karki'), ('Pratima', 'Rai'),
            ('Sandeep', 'Lamichhane'), ('Melina', 'Rai'), ('Suman', 'Shrestha'),
            ('Deepa', 'Devi')
        ]
        for first, last in student_names:
            email = f"{first.lower()}.{last.lower()}@gmail.com"
            user, created = User.objects.get_or_create(
                email=email,
                username=email.split('@')[0],
                defaults={'role': 'student', 'first_name': first, 'last_name': last}
            )
            user.set_password('password123')
            user.save()
            
            student_profile, created = Student.objects.get_or_create(user=user)
            # Enroll in 1-2 classes
            enrolled_classes = random.sample(class_objects, k=random.randint(1, 2))
            student_profile.classes.set(enrolled_classes)
            
            # Add to a random section of their first class
            target_sections = [s for s in sections if s.class_id == enrolled_classes[0]]
            if target_sections:
                random.choice(target_sections).students.add(student_profile)
        
        self.stdout.write(f'{len(student_names)} students created.')

        # 7. Create Timetable
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        for sec in sections:
            for day in days[:3]: # Just 3 days for seeding
                Timetable.objects.get_or_create(
                    section=sec,
                    day=day,
                    start_time='09:00:00',
                    end_time='10:00:00',
                    subject=random.choice(subjects),
                    teacher=random.choice(teacher_profiles)
                )
        self.stdout.write('Timetable seeded.')

        self.stdout.write(self.style.SUCCESS('Database seeded successfully with Nepali data!'))
        self.stdout.write('Credentials (Password: password123):')
        self.stdout.write('Principal: principal@gmail.com')
        self.stdout.write('Teacher: ram.sharma@gmail.com')
        self.stdout.write('Student: aryan.thapa@gmail.com')
