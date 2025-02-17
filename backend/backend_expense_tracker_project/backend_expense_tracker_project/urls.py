from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # ✅ Django Admin Panel
    path("admin/", admin.site.urls),

    # ✅ API Routes (Users, Expenses, Reports)
    path("api/", include("backend_expense_tracker_app.urls")),

    # ✅ JWT Authentication Endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # Login
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Refresh token
]
