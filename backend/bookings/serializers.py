from rest_framework import serializers
from django.utils import timezone
from .models import BookingRequest, BookingStatus
from guest_requests.models import PHONE_REGEX


class BookingRequestSerializer(serializers.ModelSerializer):
    """
    Public serializer for booking request submissions.
    Internal fields (status, admin_note, snapshots) are strictly protected.
    """
    website = serializers.CharField(required=False, allow_blank=True, write_only=True)
    special_request = serializers.CharField(required=False, allow_blank=True, max_length=5000)

    class Meta:
        model = BookingRequest
        fields = [
            'website',
            'id',
            'room',
            'room_name_snapshot',
            'price_per_night_snapshot',
            'check_in',
            'check_out',
            'adults',
            'children',
            'full_name',
            'phone',
            'email',
            'special_request',
            'status',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'room_name_snapshot',
            'price_per_night_snapshot',
            'status',
            'created_at',
        ]

    def validate_full_name(self, value):
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError("Full name is required.")
        return cleaned

    def validate_phone(self, value):
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError("Phone number is required.")
        if not PHONE_REGEX.match(cleaned) or sum(c.isdigit() for c in cleaned) < 7:
            raise serializers.ValidationError("Enter a valid phone number.")
        return cleaned

    def validate(self, attrs):
        if attrs.pop('website', '').strip():
            raise serializers.ValidationError({'website': 'Invalid submission.'})
        check_in = attrs.get('check_in')
        check_out = attrs.get('check_out')
        adults = attrs.get('adults', 1)
        children = attrs.get('children', 0)
        room = attrs.get('room')

        today = timezone.localdate()

        # Check-in cannot be in the past
        if check_in and check_in < today:
            raise serializers.ValidationError({
                'check_in': 'Check-in date cannot be in the past.'
            })

        # Check-out must be strictly after check-in
        if check_in and check_out and check_out <= check_in:
            raise serializers.ValidationError({
                'check_out': 'Check-out date must be strictly after check-in date.'
            })

        # Guest count validations
        if adults is not None and adults < 1:
            raise serializers.ValidationError({
                'adults': 'Number of adults must be at least 1.'
            })

        if children is not None and children < 0:
            raise serializers.ValidationError({
                'children': 'Number of children cannot be negative.'
            })

        # Room availability and capacity
        if room:
            if not room.is_active:
                raise serializers.ValidationError({
                    'room': 'Selected room is not currently available for booking.'
                })
            if adults and adults > room.max_adults:
                raise serializers.ValidationError({
                    'adults': f"Selected room allows at most {room.max_adults} adults."
                })
            if children is not None and children > room.max_children:
                raise serializers.ValidationError({
                    'children': f"Selected room allows at most {room.max_children} children."
                })

        return attrs

    def create(self, validated_data):
        room = validated_data['room']

        # Enforce server-side snapshotting and status
        validated_data['status'] = BookingStatus.NEW
        validated_data['room_name_snapshot'] = room.name
        validated_data['price_per_night_snapshot'] = room.price_per_night
        # Strictly ignore/strip internal administrative fields if present
        validated_data.pop('admin_note', None)

        return super().create(validated_data)
