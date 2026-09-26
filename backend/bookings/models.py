from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, F, Q
from django.utils import timezone


class BookingStatus(models.TextChoices):
    NEW = 'NEW', 'New'
    CONTACTED = 'CONTACTED', 'Contacted'
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    CANCELLED = 'CANCELLED', 'Cancelled'
    COMPLETED = 'COMPLETED', 'Completed'


class BookingRequest(models.Model):
    """
    Guest inquiry for reserving a room type.
    Must be reviewed and manually confirmed by hotel staff.
    """
    room = models.ForeignKey(
        'rooms.Room',
        on_delete=models.PROTECT,
        related_name="booking_requests",
        help_text="Requested room category"
    )
    check_in = models.DateField(help_text="Guest arrival date")
    check_out = models.DateField(help_text="Guest departure date")
    adults = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Number of adult guests (minimum 1)"
    )
    children = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Number of child guests"
    )
    full_name = models.CharField(max_length=150, help_text="Guest full name")
    phone = models.CharField(max_length=50, help_text="Guest contact phone number")
    email = models.EmailField(help_text="Guest email address")
    special_request = models.TextField(
        blank=True,
        default="",
        help_text="Optional preferences or remarks submitted by guest"
    )
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.NEW,
        help_text="Internal workflow processing state"
    )
    admin_note = models.TextField(
        blank=True,
        default="",
        help_text="Internal staff remarks (never exposed to public)"
    )
    room_name_snapshot = models.CharField(
        max_length=150,
        blank=True,
        default="",
        help_text="Historical record of room name at time of booking submission"
    )
    price_per_night_snapshot = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Historical record of nightly rate at time of booking submission"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Booking Request"
        verbose_name_plural = "Booking Requests"
        constraints = [
            CheckConstraint(
                condition=Q(adults__gte=1),
                name="booking_adults_gte_1"
            ),
            CheckConstraint(
                condition=Q(children__gte=0),
                name="booking_children_gte_0"
            ),
            CheckConstraint(
                condition=Q(check_out__gt=F('check_in')),
                name="booking_check_out_gt_check_in"
            ),
        ]

    def __str__(self):
        room_label = self.room_name_snapshot or (self.room.name if self.room_id else "No Room")
        return f"Booking #{self.id or 'New'} - {self.full_name} ({room_label})"

    def clean(self):
        super().clean()
        today = timezone.localdate()

        # Date validations
        if self._state.adding and self.check_in and self.check_in < today:
            raise ValidationError({'check_in': 'Check-in date cannot be in the past.'})
        if self.check_in and self.check_out and self.check_out <= self.check_in:
            raise ValidationError({'check_out': 'Check-out date must be strictly after check-in date.'})

        # Numeric validations
        if self.adults is not None and self.adults < 1:
            raise ValidationError({'adults': 'Number of adults must be at least 1.'})
        if self.children is not None and self.children < 0:
            raise ValidationError({'children': 'Number of children cannot be negative.'})

        # Capacity and room status validations
        if self.room_id:
            room = self.room
            if self._state.adding and not room.is_active:
                raise ValidationError({'room': 'Selected room is not currently available for booking.'})
            if self.adults and self.adults > room.max_adults:
                raise ValidationError({'adults': f"Selected room allows at most {room.max_adults} adults."})
            if self.children is not None and self.children > room.max_children:
                raise ValidationError({'children': f"Selected room allows at most {room.max_children} children."})

    def save(self, *args, **kwargs):
        # Capture historical snapshot upon creation
        if self.room_id:
            if not self.room_name_snapshot:
                self.room_name_snapshot = self.room.name
            if self.price_per_night_snapshot is None:
                self.price_per_night_snapshot = self.room.price_per_night
        super().save(*args, **kwargs)
