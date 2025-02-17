from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Expense


class ExpenseTrackerAPITest(TestCase):
    def setUp(self):
        """Setup test client and create a test user"""
        self.client = APIClient()

        # ✅ Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass", email="test@example.com")

        # ✅ Get JWT Token for authentication
        response = self.client.post('/api/login/', {"username": "testuser", "password": "testpass"}, format='json')
        self.token = response.data.get("access")

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # ✅ Create test expense
        self.expense_data = {
            "amount": 50.00,
            "category": "Food",
            "description": "Lunch",
            "date": "2024-04-05"
        }
        self.expense = Expense.objects.create(user=self.user, **self.expense_data)

    def test_user_registration(self):
        """Test user registration API"""
        response = self.client.post('/api/register/',
                                    {"username": "newuser", "password": "newpass", "email": "newuser@example.com"},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        """Test user login API"""
        response = self.client.post('/api/login/', {"username": "testuser", "password": "testpass"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_create_expense(self):
        """Test creating an expense"""
        response = self.client.post('/api/expenses/', self.expense_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_expenses(self):
        """Test retrieving expenses"""
        response = self.client.get('/api/expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_monthly_report(self):
        """Test getting a monthly expense summary"""
        response = self.client.get('/api/report/monthly/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("monthly_report", response.data)

    def test_delete_expense(self):
        """Test deleting an expense"""
        response = self.client.delete(f'/api/expense/{self.expense.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
