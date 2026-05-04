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
    help = 'Seeds the database with at least 10 entries for major models'

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
            defaults={'role': 'principal', 'first_name': 'Arun', 'last_name': 'Karki'}
        )
        principal_user.set_password('password123')
        principal_user.save()

        # 2. Create Classes (Grades 6 to 12)
        grades = [f'Grade {i}' for i in range(6, 13)]
        class_objects = []
        for g in grades:
            obj, created = Class.objects.get_or_create(name=g)
            class_objects.append(obj)

        # 3. Create 10 Teachers
        nepali_teachers = [
            ('Ram', 'Sharma'), ('Sita', 'Thapa'), ('Hari', 'Shrestha'),
            ('Gita', 'Gurung'), ('Binod', 'Tamang'), ('Anu', 'Karki'),
            ('Sunil', 'Rai'), ('Sarita', 'Lamichhane'), ('Pradeep', 'Adhikari'),
            ('Melina', 'Paudel')
        ]
        teacher_profiles = []
        for first, last in nepali_teachers:
            email = f"{first.lower()}.{last.lower()}@gmail.com"
            user = User.objects.create_user(
                email=email,
                username=email.split('@')[0],
                password='password123',
                role='teacher',
                first_name=first,
                last_name=last
            )
            profile, created = Teacher.objects.get_or_create(user=user)
            profile.classes.set(random.sample(class_objects, k=3))
            teacher_profiles.append(profile)

        # 4. Create 10 Subjects
        subject_names = [
            'Mathematics', 'Science', 'Nepali', 'Social Studies', 'English', 
            'Computer Science', 'Health & Physical Ed', 'Accountancy', 'Economics', 'Optional Math'
        ]
        subjects = []
        for name in subject_names:
            obj, created = Subject.objects.get_or_create(name=name)
            obj.classes.set(class_objects)
            obj.teachers.set(random.sample(teacher_profiles, k=2))
            subjects.append(obj)

        # 5. Create Sections (A and B for each grade)
        sections = []
        for cls in class_objects:
            for sec_name in ['A', 'B']:
                sec, created = Section.objects.get_or_create(
                    name=sec_name,
                    class_id=cls,
                    defaults={'class_teacher': random.choice(teacher_profiles)}
                )
                sections.append(sec)

        # 6. Create 20 Students (to make the lists look full)
        nepali_students = [
            ('Aryan', 'Thapa'), ('Smriti', 'Gurung'), ('Rohan', 'Shrestha'),
            ('Anjali', 'Tamang'), ('Bibek', 'Karki'), ('Pratima', 'Rai'),
            ('Sandeep', 'Lamichhane'), ('Deepa', 'Devi'), ('Suman', 'Shrestha'),
            ('Pooja', 'Adhikari'), ('Niraj', 'Paudel'), ('Ishara', 'Bhattarai'),
            ('Kiran', 'Basnet'), ('Sunita', 'Magar'), ('Bijay', 'Chaudhary'),
            ('Rashmi', 'Giri'), ('Umesh', 'Maharjan'), ('Srijana', 'Dhakal'),
            ('Bishal', 'Puri'), ('Alisha', 'Thakuri')
        ]
        for first, last in nepali_students:
            email = f"{first.lower()}.{last.lower()}@gmail.com"
            user = User.objects.create_user(
                email=email,
                username=email.split('@')[0],
                password='password123',
                role='student',
                first_name=first,
                last_name=last
            )
            student_profile, created = Student.objects.get_or_create(user=user)
            # Enroll in a random class
            target_class = random.choice(class_objects)
            student_profile.classes.add(target_class)
            
            # Add to a random section of that class
            target_sections = [s for s in sections if s.class_id == target_class]
            if target_sections:
                random.choice(target_sections).students.add(student_profile)

        # 7. Create Detailed Timetable
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        times = [
            ('09:00:00', '10:00:00'),
            ('10:00:00', '11:00:00'),
            ('11:15:00', '12:15:00'), # Post-break
            ('12:15:00', '13:15:00'),
        ]
        for sec in sections:
            for day in days:
                for start, end in times:
                    Timetable.objects.get_or_create(
                        section=sec,
                        day=day,
                        start_time=start,
                        end_time=end,
                        subject=random.choice(subjects),
                        teacher=random.choice(teacher_profiles)
                    )

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded:'))
        self.stdout.write(f'- 1 Principal (principal@gmail.com)')
        self.stdout.write(f'- {len(teacher_profiles)} Teachers')
        self.stdout.write(f'- {len(nepali_students)} Students')
        self.stdout.write(f'- {len(class_objects)} Classes (Grades 6-12)')
        self.stdout.write(f'- {len(subjects)} Subjects')
        self.stdout.write(f'- {len(sections)} Sections')
        self.stdout.write(f'- Full Timetable (Mon-Fri)')
        self.stdout.write('All passwords are: password123')
