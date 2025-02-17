from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse
import csv
from .models import Expense
from .serializers import RegisterSerializer, ExpenseSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from reportlab.pdfgen import canvas
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
import pandas as pd
from io import BytesIO
from django.core.cache import cache  # ✅ Import caching




class RegisterView(generics.CreateAPIView):
    """Handles user registration."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        """Ensure username, email, and password are properly validated"""
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response({"error": "All fields (username, email, password) are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


class UserListView(generics.ListAPIView):
    """Allows admin users to view all registered users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]  # ✅ Only admin users can access this endpoint


class ExpensePagination(PageNumberPagination):
    """Pagination for expenses"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ExpenseListView(generics.ListAPIView):
    """Handles listing expenses"""
    serializer_class = ExpenseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only the logged-in user's expenses unless admin"""
        if self.request.user.is_staff:
            return Expense.objects.all()
        return Expense.objects.filter(user=self.request.user)


class ExpenseCreateView(generics.CreateAPIView):
    """Handles creating an expense"""
    serializer_class = ExpenseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Ensure the expense is always assigned to the logged-in user"""
        serializer.save(user=self.request.user)

# provide id in ui and delete by id or date
class ExpenseDeleteView(generics.DestroyAPIView):
    """Handles deleting an expense"""
    serializer_class = ExpenseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Ensure users can only delete their own expenses unless admin"""
        if self.request.user.is_staff:
            return Expense.objects.all()
        return Expense.objects.filter(user=self.request.user)

from datetime import datetime
from django.db.models.functions import TruncMonth

class ExpenseReportPagination(PageNumberPagination):
    """Custom pagination for large reports"""
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class MonthlyReportView(generics.GenericAPIView):
    """Generates a monthly expense report with optimized queries and caching."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Fetches the monthly expense report for the logged-in user with caching."""
        month_param = request.query_params.get("month", None)
        cache_key = f"monthly_report_{request.user.id}_{month_param}"  # ✅ Unique cache key per user & month
        cached_report = cache.get(cache_key)  # ✅ Retrieve cached report if exists

        if cached_report:
            print("✅ Returning cached report")  # Debugging
            return Response({"monthly_report": cached_report}, status=status.HTTP_200_OK)

        # ✅ If no cached data, fetch from DB
        if month_param:
            try:
                selected_month = datetime.strptime(month_param, "%Y-%m").date()
            except ValueError:
                return Response({"error": "Invalid month format. Use YYYY-MM"}, status=status.HTTP_400_BAD_REQUEST)

            summary = (
                Expense.objects.filter(
                    user=request.user,
                    date__year=selected_month.year,
                    date__month=selected_month.month
                )
                .select_related("user")  # ✅ Optimized foreign key lookup
                .values("category")
                .annotate(total_spent=Sum("amount"))
            )
        else:
            summary = Expense.objects.filter(user=request.user).values("category").annotate(total_spent=Sum("amount"))

        # ✅ Store result in cache for 10 minutes (600 seconds)
        cache.set(cache_key, list(summary), timeout=600)
        print("✅ Report cached successfully")  # Debugging

        return Response({"monthly_report": list(summary)}, status=status.HTTP_200_OK)


class RecentExpensesView(generics.ListAPIView):
    """Fetches the 5 most recent expenses in descending order by date."""
    serializer_class = ExpenseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only the logged-in user's 5 most recent expenses sorted by date (desc)."""
        return Expense.objects.filter(user=self.request.user).order_by('-date')[:5]


class ExpenseUpdateView(generics.UpdateAPIView):
    """Allows users to update their existing expense details."""
    serializer_class = ExpenseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Ensure users can only update their own expenses unless they are admin."""
        if self.request.user.is_staff:
            return Expense.objects.all()
        return Expense.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        """Ensure the expense is always assigned to the logged-in user."""
        serializer.save(user=self.request.user)

class ExportPDFReportView(generics.GenericAPIView):
    """Exports expense reports as a PDF file."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Generates and downloads the PDF expense report."""
        expenses = Expense.objects.filter(user=request.user)

        if not expenses.exists():
            return Response({"message": "No expense data found."}, status=status.HTTP_404_NOT_FOUND)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="expense_report.pdf"'

        p = canvas.Canvas(response)
        y = 800
        p.drawString(100, y, "Expense Report")
        y -= 20

        for expense in expenses:
            p.drawString(100, y, f"{expense.date} - {expense.category}: ${expense.amount}")
            y -= 20

        p.save()
        return response




class ExportExcelReportView(generics.GenericAPIView):
    """Exports expense reports as an Excel file."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Generates and downloads the Excel report."""
        expenses = Expense.objects.filter(user=request.user).values("date", "category", "amount", "description")

        if not expenses.exists():
            return Response({"message": "No expense data found."}, status=status.HTTP_404_NOT_FOUND)

        df = pd.DataFrame(list(expenses))

        # Generate the Excel file in-memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Expenses")
            writer.close()

        output.seek(0)

        # Set the response headers
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="expense_report.xlsx"'
        return response

@api_view(['POST'])
def token_login(request):
    """Handles login via JWT token authentication"""
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Both username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token), "refresh": str(refresh)}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
