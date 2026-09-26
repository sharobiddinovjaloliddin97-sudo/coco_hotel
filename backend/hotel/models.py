from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, F, Q


class HotelInformation(models.Model):
    """
    Singleton model representing primary Coco Hotel information.
    Only one record is permitted in the system.
    """
    name = models.CharField(max_length=150, default="Coco Hotel", help_text="Hotel name")
    hero_image = models.ImageField(upload_to="hotel/", blank=True, help_text="Homepage cover photo")
    about_image = models.ImageField(upload_to="hotel/", blank=True, help_text="Hotel story photo")
    hero_title = models.CharField(
        max_length=200,
        default="Welcome to Coco Hotel",
        help_text="Homepage hero section main title (fallback)"
    )
    hero_title_en = models.CharField(max_length=200, blank=True, default="", help_text="Hero title in English")
    hero_title_uz = models.CharField(max_length=200, blank=True, default="", help_text="Hero title in Uzbek")
    hero_title_ru = models.CharField(max_length=200, blank=True, default="", help_text="Hero title in Russian")

    hero_subtitle = models.TextField(
        blank=True,
        default="",
        help_text="Homepage hero section supporting description (fallback)"
    )
    hero_subtitle_en = models.TextField(blank=True, default="", help_text="Hero subtitle in English")
    hero_subtitle_uz = models.TextField(blank=True, default="", help_text="Hero subtitle in Uzbek")
    hero_subtitle_ru = models.TextField(blank=True, default="", help_text="Hero subtitle in Russian")

    about_title = models.CharField(
        max_length=200,
        default="About Coco Hotel",
        help_text="About section heading (fallback)"
    )
    about_title_en = models.CharField(max_length=200, blank=True, default="", help_text="About section heading in English")
    about_title_uz = models.CharField(max_length=200, blank=True, default="", help_text="About section heading in Uzbek")
    about_title_ru = models.CharField(max_length=200, blank=True, default="", help_text="About section heading in Russian")

    about_text = models.TextField(help_text="Detailed overview and story of the hotel (fallback)")
    about_text_en = models.TextField(blank=True, default="", help_text="Detailed overview and story in English")
    about_text_uz = models.TextField(blank=True, default="", help_text="Detailed overview and story in Uzbek")
    about_text_ru = models.TextField(blank=True, default="", help_text="Detailed overview and story in Russian")

    phone = models.CharField(max_length=50, help_text="Primary contact phone number")
    secondary_phone = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="Alternative contact phone number"
    )
    email = models.EmailField(help_text="Official contact email address")
    address = models.CharField(max_length=255, help_text="Physical hotel address (fallback)")
    address_en = models.CharField(max_length=255, blank=True, default="", help_text="Physical hotel address in English")
    address_uz = models.CharField(max_length=255, blank=True, default="", help_text="Physical hotel address in Uzbek")
    address_ru = models.CharField(max_length=255, blank=True, default="", help_text="Physical hotel address in Russian")
    map_url = models.URLField(
        blank=True,
        default="",
        help_text="External link to Google Maps / Yandex Maps location"
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Geographic latitude coordinate (-90 to 90)"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Geographic longitude coordinate (-180 to 180)"
    )
    check_in_time = models.TimeField(null=True, blank=True, help_text="Standard daily check-in time")
    check_out_time = models.TimeField(null=True, blank=True, help_text="Standard daily check-out time")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hotel Information"
        verbose_name_plural = "Hotel Information"
        constraints = [
            CheckConstraint(
                condition=Q(latitude__isnull=True) | (Q(latitude__gte=-90) & Q(latitude__lte=90)),
                name="hotel_info_latitude_valid"
            ),
            CheckConstraint(
                condition=Q(longitude__isnull=True) | (Q(longitude__gte=-180) & Q(longitude__lte=180)),
                name="hotel_info_longitude_valid"
            ),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if not self.pk and HotelInformation.objects.exists():
            raise ValidationError(
                "Only one Hotel Information record is permitted. Please edit the existing record."
            )

    def save(self, *args, **kwargs):
        if not self.pk and HotelInformation.objects.exists():
            raise ValidationError(
                "Only one Hotel Information record is permitted. Please edit the existing record."
            )
        super().save(*args, **kwargs)


class Service(models.Model):
    """
    Hotel service/amenity (e.g. Wi-Fi, Breakfast, Parking).
    """
    name = models.CharField(max_length=100, unique=True, help_text="Service title (fallback)")
    name_en = models.CharField(max_length=100, blank=True, default="", help_text="Service title in English")
    name_uz = models.CharField(max_length=100, blank=True, default="", help_text="Service title in Uzbek")
    name_ru = models.CharField(max_length=100, blank=True, default="", help_text="Service title in Russian")
    description = models.TextField(blank=True, default="", help_text="Concise service description (fallback)")
    description_en = models.TextField(blank=True, default="", help_text="Service description in English")
    description_uz = models.TextField(blank=True, default="", help_text="Service description in Uzbek")
    description_ru = models.TextField(blank=True, default="", help_text="Service description in Russian")
    icon = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="Icon identifier for frontend icon mapping"
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Display order"
    )
    is_active = models.BooleanField(default=True, help_text="Whether this service is active and offered")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = "Service"
        verbose_name_plural = "Services"
        constraints = [
            CheckConstraint(
                condition=Q(sort_order__gte=0),
                name="service_sort_order_gte_0"
            )
        ]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.sort_order < 0:
            raise ValidationError({'sort_order': 'Sort order must be non-negative.'})


class GalleryImage(models.Model):
    """
    Hotel showcase image displayed in the website photo gallery.
    """
    category = models.CharField(max_length=20, default='interior', choices=[
        ('rooms', 'Rooms'), ('interior', 'Interior'), ('dining', 'Dining'), ('exterior', 'Exterior')
    ])
    image = models.ImageField(upload_to="gallery/", help_text="Upload gallery image")
    title = models.CharField(max_length=150, blank=True, default="", help_text="Optional image title (fallback)")
    title_en = models.CharField(max_length=150, blank=True, default="", help_text="Optional image title in English")
    title_uz = models.CharField(max_length=150, blank=True, default="", help_text="Optional image title in Uzbek")
    title_ru = models.CharField(max_length=150, blank=True, default="", help_text="Optional image title in Russian")
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="Accessible image description (fallback)"
    )
    alt_text_en = models.CharField(max_length=200, blank=True, default="", help_text="Accessible image description in English")
    alt_text_uz = models.CharField(max_length=200, blank=True, default="", help_text="Accessible image description in Uzbek")
    alt_text_ru = models.CharField(max_length=200, blank=True, default="", help_text="Accessible image description in Russian")
    sort_order = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Display order in gallery"
    )
    is_active = models.BooleanField(default=True, help_text="Whether this image appears in the gallery")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
        constraints = [
            CheckConstraint(
                condition=Q(sort_order__gte=0),
                name="gallery_image_sort_order_gte_0"
            )
        ]

    def __str__(self):
        return self.title or f"Gallery Image #{self.id or 'new'}"

    def clean(self):
        super().clean()
        if self.sort_order < 0:
            raise ValidationError({'sort_order': 'Sort order must be non-negative.'})


class Promotion(models.Model):
    """
    Special offer or promotion for Coco Hotel.
    """
    title = models.CharField(max_length=150, help_text="Offer headline (fallback)")
    title_en = models.CharField(max_length=150, blank=True, default="", help_text="Offer headline in English")
    title_uz = models.CharField(max_length=150, blank=True, default="", help_text="Offer headline in Uzbek")
    title_ru = models.CharField(max_length=150, blank=True, default="", help_text="Offer headline in Russian")
    slug = models.SlugField(max_length=160, unique=True, help_text="URL-safe unique identifier")
    short_description = models.CharField(max_length=300, help_text="Concise summary for promotion cards (fallback)")
    short_description_en = models.CharField(max_length=300, blank=True, default="", help_text="Summary in English")
    short_description_uz = models.CharField(max_length=300, blank=True, default="", help_text="Summary in Uzbek")
    short_description_ru = models.CharField(max_length=300, blank=True, default="", help_text="Summary in Russian")
    description = models.TextField(help_text="Full promotional details and terms (fallback)")
    description_en = models.TextField(blank=True, default="", help_text="Full promotional details and terms in English")
    description_uz = models.TextField(blank=True, default="", help_text="Full promotional details and terms in Uzbek")
    description_ru = models.TextField(blank=True, default="", help_text="Full promotional details and terms in Russian")
    image = models.ImageField(
        upload_to="promotions/",
        null=True,
        blank=True,
        help_text="Promotional banner image"
    )
    valid_from = models.DateField(
        null=True,
        blank=True,
        help_text="Start date of promotion (optional)"
    )
    valid_until = models.DateField(
        null=True,
        blank=True,
        help_text="End date of promotion (optional)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Master toggle for promotion availability"
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Display order"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"
        constraints = [
            CheckConstraint(
                condition=Q(sort_order__gte=0),
                name="promotion_sort_order_gte_0"
            ),
            CheckConstraint(
                condition=Q(valid_from__isnull=True) | Q(valid_until__isnull=True) | Q(valid_until__gte=F('valid_from')),
                name="promotion_valid_until_gte_valid_from"
            ),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.sort_order < 0:
            raise ValidationError({'sort_order': 'Sort order must be non-negative.'})
        if self.valid_from and self.valid_until and self.valid_until < self.valid_from:
            raise ValidationError({
                'valid_until': 'valid_until must be on or after valid_from.'
            })
