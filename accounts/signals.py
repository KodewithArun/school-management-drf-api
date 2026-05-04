from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from students.models import Student
from teachers.models import Teacher

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a Student or Teacher profile 
    whenever a new User is created with that role.
    """
    if created:
        if instance.role == 'student':
            Student.objects.get_or_create(user=instance)
        elif instance.role == 'teacher':
            Teacher.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Ensures the profile is saved when the user is updated.
    """
    if instance.role == 'student':
        if hasattr(instance, 'student'):
            instance.student.save()
    elif instance.role == 'teacher':
        if hasattr(instance, 'teacher'):
            instance.teacher.save()
