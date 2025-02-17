from django.urls import path
from .views import (
    RegisterView, UserListView, ExpenseListView, ExpenseCreateView, ExpenseDeleteView,
    MonthlyReportView, token_login, RecentExpensesView, ExpenseUpdateView,
    ExportExcelReportView, ExportPDFReportView, ExportExcelReportView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # ✅ User Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', token_login, name='token_obtain_pair'),  # Custom login view for JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ Expense Endpoints
    path('expenses/list/', ExpenseListView.as_view(), name='list_expenses'),  # 🔹 Lists expenses
    path('expenses/create/', ExpenseCreateView.as_view(), name='create_expense'),  # 🔹 Creates an expense
    path('expenses/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='delete_expense'),  # 🔹 Deletes an expense

    # ✅ Recent Expenses (Last 5)
    path('expenses/recent/', RecentExpensesView.as_view(), name='recent_expenses'),

    # ✅ Edit an existing expense
    path('expenses/<int:pk>/update/', ExpenseUpdateView.as_view(), name='update_expense'),

    # # ✅ Report Endpoints (Fixed Export URL)
    path('report/monthly/', MonthlyReportView.as_view(), name='monthly_report'),
    # path('report/download/', ExportReportView.as_view(), name='export_report'),  # ✅ Fixed: Added trailing slash

# ✅ Separate endpoints for CSV and Excel downloads
    # ✅ Export Reports
    path('report/download/pdf/', ExportPDFReportView.as_view(), name='export_pdf_report'),
    path('report/download/excel/', ExportExcelReportView.as_view(), name='export_excel_report'),


    # ✅ Admin - Get All Users (Admin Only)
    path('users/', UserListView.as_view(), name='user_list'),
]
