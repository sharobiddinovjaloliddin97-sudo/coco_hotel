from decimal import Decimal
import io
from PIL import Image

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rooms.models import Amenity, Room, RoomImage


def create_dummy_image(name='test.jpg'):
    """Generate a minimal valid 1x1 image for testing."""
    file = io.BytesIO()
    image = Image.new('RGB', (1, 1), color='red')
    image.save(file, 'JPEG')
    file.seek(0)
    return SimpleUploadedFile(name, file.read(), content_type='image/jpeg')


class RoomModelTests(APITestCase):
    """
    Validation and database constraint tests for Room, Amenity, and RoomImage.
    """

    def setUp(self):
        self.amenity = Amenity.objects.create(name="Free Wi-Fi", icon="wifi", sort_order=1)

    def test_create_valid_room(self):
        room = Room.objects.create(
            name="Deluxe Double",
            slug="deluxe-double",
            short_description="Comfortable room with queen bed",
            description="Full description of deluxe double room with balcony.",
            price_per_night=Decimal("650000.00"),
            max_adults=2,
            max_children=1,
            bed_type="1 Queen Bed",
            room_size=Decimal("28.50"),
            is_featured=True,
            is_active=True,
            sort_order=10
        )
        room.amenities.add(self.amenity)
        room.full_clean()
        self.assertEqual(room.name, "Deluxe Double")
        self.assertEqual(str(room), "Deluxe Double")
        self.assertEqual(room.amenities.count(), 1)

    def test_negative_price_rejected(self):
        room = Room(
            name="Invalid Price",
            slug="invalid-price",
            short_description="Short",
            description="Long",
            price_per_night=Decimal("-10.00"),
            max_adults=2,
            bed_type="King"
        )
        with self.assertRaises(ValidationError):
            room.full_clean()

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                room.save()

    def test_max_adults_below_one_rejected(self):
        room = Room(
            name="Zero Adults",
            slug="zero-adults",
            short_description="Short",
            description="Long",
            price_per_night=Decimal("500000.00"),
            max_adults=0,
            bed_type="King"
        )
        with self.assertRaises(ValidationError):
            room.full_clean()

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                room.save()

    def test_negative_max_children_rejected(self):
        room = Room(
            name="Negative Children",
            slug="negative-children",
            short_description="Short",
            description="Long",
            price_per_night=Decimal("500000.00"),
            max_adults=2,
            max_children=-1,
            bed_type="King"
        )
        with self.assertRaises(ValidationError):
            room.full_clean()

    def test_invalid_room_size_rejected(self):
        room = Room(
            name="Zero Size",
            slug="zero-size",
            short_description="Short",
            description="Long",
            price_per_night=Decimal("500000.00"),
            max_adults=2,
            room_size=Decimal("0.00"),
            bed_type="King"
        )
        with self.assertRaises(ValidationError):
            room.full_clean()

    def test_primary_image_uniqueness_enforced(self):
        room = Room.objects.create(
            name="Suite",
            slug="suite",
            short_description="Luxury suite",
            description="Spacious luxury suite",
            price_per_night=Decimal("1200000.00"),
            max_adults=3,
            bed_type="1 King Bed"
        )
        img1 = RoomImage.objects.create(
            room=room,
            image=create_dummy_image("img1.jpg"),
            is_primary=True,
            sort_order=1
        )
        img1.full_clean()

        # Second primary image should be rejected by model clean() and DB constraint
        img2 = RoomImage(
            room=room,
            image=create_dummy_image("img2.jpg"),
            is_primary=True,
            sort_order=2
        )
        with self.assertRaises(ValidationError):
            img2.full_clean()

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                img2.save()

    def test_primary_image_property_fallback(self):
        room = Room.objects.create(
            name="Standard Room",
            slug="standard-room",
            short_description="Simple room",
            description="Standard room description",
            price_per_night=Decimal("400000.00"),
            max_adults=2,
            bed_type="Twin Beds"
        )
        # Without primary flag, falls back to first image
        img = RoomImage.objects.create(
            room=room,
            image=create_dummy_image("fallback.jpg"),
            is_primary=False,
            sort_order=5
        )
        self.assertEqual(room.primary_image, img)


class RoomAPITests(APITestCase):
    """
    API endpoint tests for public /api/v1/rooms/ and /api/v1/rooms/<slug>/.
    """

    def setUp(self):
        self.amenity_wifi = Amenity.objects.create(name="High-speed Wi-Fi", icon="wifi", sort_order=1)
        self.amenity_ac = Amenity.objects.create(name="Air Conditioning", icon="snowflake", sort_order=2)

        self.active_featured = Room.objects.create(
            name="Standard Double",
            slug="standard-double",
            short_description="Cozy standard room",
            description="Detailed standard double description.",
            price_per_night=Decimal("500000.00"),
            max_adults=2,
            max_children=1,
            bed_type="1 Queen Bed",
            room_size=Decimal("22.00"),
            is_featured=True,
            is_active=True,
            sort_order=1
        )
        self.active_featured.amenities.add(self.amenity_wifi, self.amenity_ac)

        self.img_primary = RoomImage.objects.create(
            room=self.active_featured,
            image=create_dummy_image("std_primary.jpg"),
            alt_text="Standard room bedroom view",
            is_primary=True,
            sort_order=0
        )
        self.img_gallery = RoomImage.objects.create(
            room=self.active_featured,
            image=create_dummy_image("std_bath.jpg"),
            alt_text="Standard room bathroom",
            is_primary=False,
            sort_order=1
        )

        self.active_regular = Room.objects.create(
            name="Family Suite",
            slug="family-suite",
            short_description="Large suite for families",
            description="Detailed family suite description.",
            price_per_night=Decimal("950000.00"),
            max_adults=4,
            max_children=2,
            bed_type="2 Queen Beds",
            room_size=Decimal("45.00"),
            is_featured=False,
            is_active=True,
            sort_order=2
        )

        self.inactive_room = Room.objects.create(
            name="Under Renovation",
            slug="under-renovation",
            short_description="Not available currently",
            description="Closed room description.",
            price_per_night=Decimal("300000.00"),
            max_adults=1,
            max_children=0,
            bed_type="Single Bed",
            is_featured=True,
            is_active=False,
            sort_order=99
        )

        self.list_url = reverse('rooms:room-list')

    def test_room_list_returns_200_and_only_active_rooms(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only return the 2 active rooms
        self.assertEqual(len(response.data), 2)
        slugs = [item['slug'] for item in response.data]
        self.assertIn("standard-double", slugs)
        self.assertIn("family-suite", slugs)
        self.assertNotIn("under-renovation", slugs)

    def test_room_list_featured_filter(self):
        # ?featured=true
        response_featured = self.client.get(self.list_url, {'featured': 'true'})
        self.assertEqual(response_featured.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_featured.data), 1)
        self.assertEqual(response_featured.data[0]['slug'], "standard-double")

        # ?featured=false
        response_regular = self.client.get(self.list_url, {'featured': 'false'})
        self.assertEqual(response_regular.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_regular.data), 1)
        self.assertEqual(response_regular.data[0]['slug'], "family-suite")

    def test_room_detail_returns_active_room_details(self):
        detail_url = reverse('rooms:room-detail', kwargs={'slug': 'standard-double'})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['name'], "Standard Double")
        self.assertEqual(data['slug'], "standard-double")
        self.assertEqual(Decimal(str(data['price_per_night'])), Decimal("500000.00"))
        self.assertEqual(data['max_adults'], 2)
        self.assertEqual(data['max_children'], 1)
        self.assertEqual(len(data['amenities']), 2)
        self.assertEqual(data['primary_image']['id'], self.img_primary.id)
        self.assertEqual(len(data['images']), 2)

    def test_room_detail_returns_404_for_inactive_room(self):
        detail_url = reverse('rooms:room-detail', kwargs={'slug': 'under-renovation'})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_room_detail_returns_404_for_unknown_slug(self):
        detail_url = reverse('rooms:room-detail', kwargs={'slug': 'does-not-exist'})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_write_protection_on_list(self):
        for method in ['post', 'put', 'patch', 'delete']:
            client_method = getattr(self.client, method)
            response = client_method(self.list_url, {'name': 'Hacked Room'})
            self.assertEqual(
                response.status_code,
                status.HTTP_405_METHOD_NOT_ALLOWED,
                f"Method {method.upper()} on list should return 405"
            )

    def test_public_write_protection_on_detail(self):
        detail_url = reverse('rooms:room-detail', kwargs={'slug': 'standard-double'})
        for method in ['post', 'put', 'patch', 'delete']:
            client_method = getattr(self.client, method)
            response = client_method(detail_url, {'name': 'Hacked Room'})
            self.assertEqual(
                response.status_code,
                status.HTTP_405_METHOD_NOT_ALLOWED,
                f"Method {method.upper()} on detail should return 405"
            )
