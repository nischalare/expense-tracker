from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)  # ✅ Setup logging

class BackendExpenseTrackerAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend_expense_tracker_app"
    verbose_name = "Expense Tracker App"

    def ready(self):
        """Runs when the app is ready (useful for signals & startup tasks)."""
        try:
            import backend_expense_tracker_app.signals  # ✅ Load signals dynamically
            logger.info("✅ Signals loaded successfully for Expense Tracker App.")
        except Exception as e:
            logger.error(f"❌ Error loading signals: {e}")


