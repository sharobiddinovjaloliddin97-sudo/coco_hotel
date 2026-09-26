from django.urls import path
from .views import CallbackRequestCreateView, ContactMessageCreateView

urlpatterns = [
    path('callback-requests/', CallbackRequestCreateView.as_view(), name='callback-request-create'),
    path('contact-messages/', ContactMessageCreateView.as_view(), name='contact-message-create'),
]
