import re
from django.core.exceptions import ValidationError
from django.db import models


PHONE_REGEX = re.compile(r'^[0-9+\s\-()]{7,50}$')


def validate_phone_number(value):
    cleaned = value.strip()
    if not cleaned:
        raise ValidationError('Phone number is required.')
    if not PHONE_REGEX.match(cleaned):
        raise ValidationError('Enter a valid phone number containing digits, +, spaces, parentheses, or hyphens.')


class RequestStatus(models.TextChoices):
    NEW = 'NEW', 'New'
    CONTACTED = 'CONTACTED', 'Contacted'
    CLOSED = 'CLOSED', 'Closed'


class CallbackRequest(models.Model):
    """
    Guest request for a phone call back from hotel staff.
    """
    full_name = models.CharField(max_length=150, help_text="Guest full name")
    phone = models.CharField(max_length=50, help_text="Contact phone number")
    preferred_time = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="Preferred time window for callback (e.g. 'Morning', 'After 18:00')"
    )
    message = models.TextField(
        blank=True,
        default="",
        help_text="Optional remarks or inquiry submitted by guest"
    )
    status = models.CharField(
        max_length=20,
        choices=RequestStatus.choices,
        default=RequestStatus.NEW,
        help_text="Internal workflow processing state"
    )
    admin_note = models.TextField(
        blank=True,
        default="",
        help_text="Internal staff remarks (never exposed to public)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Callback Request"
        verbose_name_plural = "Callback Requests"

    def __str__(self):
        return f"Callback #{self.id or 'New'} - {self.full_name} ({self.phone})"

    def clean(self):
        super().clean()
        if self.full_name:
            self.full_name = self.full_name.strip()
            if not self.full_name:
                raise ValidationError({'full_name': 'Full name is required.'})
        else:
            raise ValidationError({'full_name': 'Full name is required.'})

        if self.phone:
            self.phone = self.phone.strip()
            if not self.phone:
                raise ValidationError({'phone': 'Phone number is required.'})
            if not PHONE_REGEX.match(self.phone):
                raise ValidationError({'phone': 'Enter a valid phone number.'})
        else:
            raise ValidationError({'phone': 'Phone number is required.'})

        if self.preferred_time:
            self.preferred_time = self.preferred_time.strip()
        if self.message:
            self.message = self.message.strip()

    def save(self, *args, **kwargs):
        if self.full_name:
            self.full_name = self.full_name.strip()
        if self.phone:
            self.phone = self.phone.strip()
        if self.preferred_time:
            self.preferred_time = self.preferred_time.strip()
        if self.message:
            self.message = self.message.strip()
        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    """
    General guest inquiry message submitted through website contact form.
    """
    full_name = models.CharField(max_length=150, help_text="Guest full name")
    email = models.EmailField(help_text="Guest contact email address")
    phone = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="Optional contact phone number"
    )
    subject = models.CharField(max_length=200, help_text="Subject of message")
    message = models.TextField(help_text="Message body submitted by guest")
    status = models.CharField(
        max_length=20,
        choices=RequestStatus.choices,
        default=RequestStatus.NEW,
        help_text="Internal workflow processing state"
    )
    admin_note = models.TextField(
        blank=True,
        default="",
        help_text="Internal staff remarks (never exposed to public)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"Message #{self.id or 'New'} - {self.full_name}: {self.subject}"

    def clean(self):
        super().clean()
        if self.full_name:
            self.full_name = self.full_name.strip()
            if not self.full_name:
                raise ValidationError({'full_name': 'Full name is required.'})
        else:
            raise ValidationError({'full_name': 'Full name is required.'})

        if self.subject:
            self.subject = self.subject.strip()
            if not self.subject:
                raise ValidationError({'subject': 'Subject cannot be empty.'})
        else:
            raise ValidationError({'subject': 'Subject is required.'})

        if self.message:
            self.message = self.message.strip()
            if not self.message:
                raise ValidationError({'message': 'Message cannot be empty.'})
        else:
            raise ValidationError({'message': 'Message is required.'})

        if self.phone:
            self.phone = self.phone.strip()
            if self.phone and not PHONE_REGEX.match(self.phone):
                raise ValidationError({'phone': 'Enter a valid phone number.'})

    def save(self, *args, **kwargs):
        if self.full_name:
            self.full_name = self.full_name.strip()
        if self.subject:
            self.subject = self.subject.strip()
        if self.message:
            self.message = self.message.strip()
        if self.phone:
            self.phone = self.phone.strip()
        super().save(*args, **kwargs)
