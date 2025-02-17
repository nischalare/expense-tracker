from django.contrib import admin
from .models import Expense
from django.contrib.auth.models import User

# ✅ Register Expense Model
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'category', 'date', 'description')
    search_fields = ('user__username', 'category')
    list_filter = ('category', 'date')

# ✅ Register User Model (if needed)
admin.site.site_header = "Expense Tracker Admin"
admin.site.site_title = "Expense Tracker Admin Portal"
admin.site.index_title = "Welcome to the Expense Tracker Admin Panel"
