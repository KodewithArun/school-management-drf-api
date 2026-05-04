# students/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Student
from classes.models import Class

User = get_user_model()

class StudentAPITest(APITestCase):
    
    def setUp(self):
        # setUp() runs BEFORE every test. We use it to populate our blank test database.
        
        # 1. Create a mock user
        self.user = User.objects.create_user(
            username="teststudent", 
            email="test@student.com", 
            password="password123",
            role="student"
        )
        
        # 2. Create a mock student profile linked to the user
        self.student = Student.objects.create(user=self.user)
        
        # 3. Create a mock class and link it
        self.mock_class = Class.objects.create(name="Grade 10")
        self.student.classes.add(self.mock_class)

    def test_get_students_list(self):
        # 1. Simulate a GET request to the explicit URL the router built
        response = self.client.get('/api/students/')
        
        # 2. ASSERT: Did the server return a 200 OK?
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 3. ASSERT: Did our pagination work? (Should have 'count', 'next', 'results')
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        
        # 4. ASSERT: Did it actually find the 1 student we created in setUp()?
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['user_details']['email'], 'test@student.com')
