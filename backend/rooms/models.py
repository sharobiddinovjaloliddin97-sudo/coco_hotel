from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint


class Amenity(models.Model):
    """
    Amenity available in hotel rooms (e.g., Wi-Fi, Air Conditioning, Balcony).
    """
    name = models.CharField(max_length=100, unique=True, help_text="Human-readable amenity name (fallback)")
    name_en = models.CharField(max_length=100, blank=True, default="", help_text="Amenity name in English")
    name_uz = models.CharField(max_length=100, blank=True, default="", help_text="Amenity name in Uzbek")
    name_ru = models.CharField(max_length=100, blank=True, default="", help_text="Amenity name in Russian")
    icon = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="Optional icon identifier for frontend icon mapping (e.g., 'wifi', 'tv')"
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Display order in lists"
    )
    is_active = models.BooleanField(default=True, help_text="Whether this amenity is currently active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"
        constraints = [
            CheckConstraint(
                check=Q(sort_order__gte=0),
                name="amenity_sort_order_gte_0"
            )
        ]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.sort_order < 0:
            raise ValidationError({'sort_order': 'Sort order must be non-negative.'})


class Room(models.Model):
    """
    Room category / type shown to hotel guests on the website.
    """
    name = models.CharField(max_length=150, help_text="Room category title (fallback)")
    name_en = models.CharField(max_length=150, blank=True, default="", help_text="Room category title in English")
    name_uz = models.CharField(max_length=150, blank=True, default="", help_text="Room category title in Uzbek")
    name_ru = models.CharField(max_length=150, blank=True, default="", help_text="Room category title in Russian")
    slug = models.SlugField(max_length=160, unique=True, help_text="URL-safe unique identifier")
    short_description = models.CharField(max_length=300, help_text="Concise room overview (fallback)")
    short_description_en = models.CharField(max_length=300, blank=True, default="", help_text="Concise room overview in English")
    short_description_uz = models.CharField(max_length=300, blank=True, default="", help_text="Concise room overview in Uzbek")
    short_description_ru = models.CharField(max_length=300, blank=True, default="", help_text="Concise room overview in Russian")
    description = models.TextField(help_text="Full detailed room description (fallback)")
    description_en = models.TextField(blank=True, default="", help_text="Full detailed room description in English")
    description_uz = models.TextField(blank=True, default="", help_text="Full detailed room description in Uzbek")
    description_ru = models.TextField(blank=True, default="", help_text="Full detailed room description in Russian")
    price_per_night = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Nightly price in local currency (UZS)"
    )
    max_adults = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Maximum adult capacity (at least 1)"
    )
    max_children = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Maximum child capacity"
    )
    bed_type = models.CharField(max_length=100, help_text="Bed arrangement description (fallback)")
    bed_type_en = models.CharField(max_length=100, blank=True, default="", help_text="Bed arrangement in English")
    bed_type_uz = models.CharField(max_length=100, blank=True, default="", help_text="Bed arrangement in Uzbek")
    bed_type_ru = models.CharField(max_length=100, blank=True, default="", help_text="Bed arrangement in Russian")
    room_size = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Room area in square meters (m²)"
    )
    amenities = models.ManyToManyField(
        Amenity,
        blank=True,
        related_name="rooms",
        help_text="Amenities available in this room type"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Feature this room on homepage/highlights"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Controls public visibility on the website"
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Display order in catalogue"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        constraints = [
            CheckConstraint(
                check=Q(price_per_night__gte=0),
                name="room_price_gte_0"
            ),
            CheckConstraint(
                check=Q(max_adults__gte=1),
                name="room_max_adults_gte_1"
            ),
            CheckConstraint(
                check=Q(max_children__gte=0),
                name="room_max_children_gte_0"
            ),
            CheckConstraint(
                check=Q(sort_order__gte=0),
                name="room_sort_order_gte_0"
            ),
            CheckConstraint(
                check=Q(room_size__isnull=True) | Q(room_size__gt=0),
                name="room_size_gt_0"
            ),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.price_per_night is not None and self.price_per_night < Decimal('0.00'):
            raise ValidationError({'price_per_night': 'Price per night must not be negative.'})
        if self.max_adults is not None and self.max_adults < 1:
            raise ValidationError({'max_adults': 'Max adults must be at least 1.'})
        if self.max_children is not None and self.max_children < 0:
            raise ValidationError({'max_children': 'Max children must be non-negative.'})
        if self.sort_order is not None and self.sort_order < 0:
            raise ValidationError({'sort_order': 'Sort order must be non-negative.'})
        if self.room_size is not None and self.room_size <= Decimal('0.00'):
            raise ValidationError({'room_size': 'Room size must be greater than zero.'})

    @property
    def primary_image(self):
        """Returns the designated primary image, or falls back to first sorted image."""
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary
        return self.images.first()


class RoomImage(models.Model):
    """
    Image for a room category, with primary designation.
    """
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="rooms/")
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="Accessible image description"
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Mark as the main display image for this room"
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Gallery order"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = "Room Image"
        verbose_name_plural = "Room Images"
        constraints = [
            CheckConstraint(
                check=Q(sort_order__gte=0),
                name="room_image_sort_order_gte_0"
            ),
            UniqueConstraint(
                fields=['room'],
                condition=Q(is_primary=True),
                name="unique_primary_image_per_room"
            ),
        ]

    def __str__(self):
        room_name = self.room.name if self.room_id else "Unassigned"
        image_type = "Primary" if self.is_primary else "Gallery"
        return f"{room_name} Image ({image_type})"

    def clean(self):
        super().clean()
        if self.sort_order < 0:
            raise ValidationError({'sort_order': 'Sort order must be non-negative.'})
        if self.is_primary and self.room_id:
            existing = RoomImage.objects.filter(
                room_id=self.room_id,
                is_primary=True
            ).exclude(pk=self.pk).exists()
            if existing:
                raise ValidationError({
                    'is_primary': 'Another primary image already exists for this room.'
                })
