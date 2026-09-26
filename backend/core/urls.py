from django.urls import path
from core.views import HealthCheckView
from core.ai_views import AIChatView

app_name = 'core'

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('ai/chat/', AIChatView.as_view(), name='ai-chat'),
]
