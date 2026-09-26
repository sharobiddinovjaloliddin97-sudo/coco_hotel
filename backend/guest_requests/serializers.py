from rest_framework import serializers
from .models import CallbackRequest, ContactMessage, RequestStatus, PHONE_REGEX


class CallbackRequestSerializer(serializers.ModelSerializer):
    """
    Public serializer for guest callback requests.
    Includes honeypot anti-spam protection and protected administrative fields.
    """
    website = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        write_only=True,
        help_text="Anti-spam honeypot field (must remain empty)"
    )

    class Meta:
        model = CallbackRequest
        fields = [
            'id',
            'full_name',
            'phone',
            'preferred_time',
            'message',
            'status',
            'created_at',
            'website',
        ]
        read_only_fields = [
            'id',
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
        if not PHONE_REGEX.match(cleaned):
            raise serializers.ValidationError(
                "Enter a valid phone number containing digits, +, spaces, parentheses, or hyphens."
            )
        return cleaned

    def validate(self, attrs):
        website = attrs.pop('website', '')
        if website and str(website).strip():
            raise serializers.ValidationError({"website": "Invalid submission."})
        return attrs

    def create(self, validated_data):
        # Force default initial status and purge any internal administrative notes
        validated_data['status'] = RequestStatus.NEW
        validated_data.pop('admin_note', None)
        return super().create(validated_data)


class ContactMessageSerializer(serializers.ModelSerializer):
    """
    Public serializer for guest contact messages.
    Includes honeypot anti-spam protection and protected administrative fields.
    """
    website = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        write_only=True,
        help_text="Anti-spam honeypot field (must remain empty)"
    )

    class Meta:
        model = ContactMessage
        fields = [
            'id',
            'full_name',
            'email',
            'phone',
            'subject',
            'message',
            'status',
            'created_at',
            'website',
        ]
        read_only_fields = [
            'id',
            'status',
            'created_at',
        ]

    def validate_full_name(self, value):
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError("Full name is required.")
        return cleaned

    def validate_subject(self, value):
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError("Subject cannot be empty.")
        return cleaned

    def validate_message(self, value):
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError("Message cannot be empty.")
        return cleaned

    def validate_phone(self, value):
        cleaned = value.strip()
        if cleaned and not PHONE_REGEX.match(cleaned):
            raise serializers.ValidationError(
                "Enter a valid phone number containing digits, +, spaces, parentheses, or hyphens."
            )
        return cleaned

    def validate(self, attrs):
        website = attrs.pop('website', '')
        if website and str(website).strip():
            raise serializers.ValidationError({"website": "Invalid submission."})
        return attrs

    def create(self, validated_data):
        validated_data['status'] = RequestStatus.NEW
        validated_data.pop('admin_note', None)
        return super().create(validated_data)
