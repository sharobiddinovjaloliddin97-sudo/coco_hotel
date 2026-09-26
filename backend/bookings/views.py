from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from .models import BookingRequest
from .serializers import BookingRequestSerializer


class BookingRequestCreateView(generics.CreateAPIView):
    """
    Public endpoint for submitting booking inquiries.
    Restricted to POST only; visitors cannot list or inspect bookings.
    Includes throttling and rapid duplicate submission protection.
    """
    queryset = BookingRequest.objects.none()
    serializer_class = BookingRequestSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'booking_submission'

    DUPLICATE_WINDOW_SECONDS = getattr(settings, 'BOOKING_DUPLICATE_WINDOW_SECONDS', 120)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = serializer.validated_data['room']
        check_in = serializer.validated_data['check_in']
        check_out = serializer.validated_data['check_out']
        full_name = serializer.validated_data['full_name'].strip()
        phone = serializer.validated_data['phone'].strip()
        email = serializer.validated_data['email'].strip()

        # Rapid duplicate submission protection
        window_start = timezone.now() - timedelta(seconds=self.DUPLICATE_WINDOW_SECONDS)
        duplicate = BookingRequest.objects.filter(
            room=room,
            check_in=check_in,
            check_out=check_out,
            full_name__iexact=full_name,
            phone=phone,
            email__iexact=email,
            created_at__gte=window_start,
        ).order_by('-created_at').first()

        if duplicate:
            response_serializer = self.get_serializer(duplicate)
            data = response_serializer.data
            data['detail'] = "Your booking request has already been received and is being processed by hotel staff."
            data['message'] = "Your booking request has already been received and is being processed by hotel staff."
            return Response(data, status=status.HTTP_200_OK)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
