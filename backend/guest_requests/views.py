from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from .models import CallbackRequest, ContactMessage
from .serializers import CallbackRequestSerializer, ContactMessageSerializer


class CallbackRequestCreateView(generics.CreateAPIView):
    """
    Public endpoint for submitting callback requests.
    Restricted to POST only; visitors cannot list or inspect requests.
    Includes throttling and rapid duplicate submission protection.
    """
    queryset = CallbackRequest.objects.none()
    serializer_class = CallbackRequestSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'callback_submission'

    DUPLICATE_WINDOW_SECONDS = getattr(settings, 'CALLBACK_DUPLICATE_WINDOW_SECONDS', 120)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        full_name = serializer.validated_data['full_name'].strip()
        phone = serializer.validated_data['phone'].strip()
        message = serializer.validated_data.get('message', '').strip()

        # Rapid duplicate submission protection
        window_start = timezone.now() - timedelta(seconds=self.DUPLICATE_WINDOW_SECONDS)
        duplicate = CallbackRequest.objects.filter(
            full_name__iexact=full_name,
            phone=phone,
            message=message,
            created_at__gte=window_start,
        ).order_by('-created_at').first()

        if duplicate:
            response_serializer = self.get_serializer(duplicate)
            data = response_serializer.data
            data['detail'] = "Your callback request has already been received and will be reviewed by hotel staff."
            data['message'] = "Your callback request has already been received and will be reviewed by hotel staff."
            return Response(data, status=status.HTTP_200_OK)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        data['detail'] = "Your callback request has been received."
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class ContactMessageCreateView(generics.CreateAPIView):
    """
    Public endpoint for submitting contact messages.
    Restricted to POST only; visitors cannot list or inspect messages.
    Includes throttling and rapid duplicate submission protection.
    """
    queryset = ContactMessage.objects.none()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'contact_submission'

    DUPLICATE_WINDOW_SECONDS = getattr(settings, 'CONTACT_DUPLICATE_WINDOW_SECONDS', 120)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        full_name = serializer.validated_data['full_name'].strip()
        email = serializer.validated_data['email'].strip()
        subject = serializer.validated_data['subject'].strip()
        message = serializer.validated_data['message'].strip()

        # Rapid duplicate submission protection
        window_start = timezone.now() - timedelta(seconds=self.DUPLICATE_WINDOW_SECONDS)
        duplicate = ContactMessage.objects.filter(
            full_name__iexact=full_name,
            email__iexact=email,
            subject__iexact=subject,
            message=message,
            created_at__gte=window_start,
        ).order_by('-created_at').first()

        if duplicate:
            response_serializer = self.get_serializer(duplicate)
            data = response_serializer.data
            data['detail'] = "Your message has already been received and will be reviewed by hotel staff."
            data['message'] = "Your message has already been received and will be reviewed by hotel staff."
            return Response(data, status=status.HTTP_200_OK)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        data['detail'] = "Your message has been received."
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
