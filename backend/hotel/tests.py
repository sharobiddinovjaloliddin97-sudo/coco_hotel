from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from hotel.models import HotelInformation, Service, GalleryImage, Promotion
from rooms.tests import create_dummy_image


class HotelInformationTests(APITestCase):
    """
    Test suite for HotelInformation singleton behavior and API endpoint.
    """

    def test_get_hotel_info_empty_handled_gracefully(self):
        url = reverse('hotel:hotel-info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Coco Hotel')

    def test_valid_hotel_info_and_api_return(self):
        HotelInformation.objects.create(
            name="Coco Hotel Tashkent",
            hero_title="Welcome to Luxury",
            hero_subtitle="Your home away from home",
            about_title="Experience Comfort",
            about_text="Full hotel history and vision.",
            phone="+998 71 123 4567",
            secondary_phone="+998 71 123 4568",
            email="info@coco-hotel.uz",
            address="123 Amir Temur Street, Tashkent, Uzbekistan",
            map_url="https://maps.google.com/?q=coco-hotel",
            latitude=Decimal("41.311081"),
            longitude=Decimal("69.240562"),
        )
        url = reverse('hotel:hotel-info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Coco Hotel Tashkent")
        self.assertEqual(response.data['email'], "info@coco-hotel.uz")
        self.assertEqual(response.data['phone'], "+998 71 123 4567")

    def test_singleton_protection(self):
        HotelInformation.objects.create(
            name="Primary Hotel",
            phone="+998 71 111 1111",
            email="primary@coco-hotel.uz",
            address="Primary Address",
            about_text="Primary About"
        )
        second = HotelInformation(
            name="Duplicate Hotel",
            phone="+998 71 222 2222",
            email="duplicate@coco-hotel.uz",
            address="Duplicate Address",
            about_text="Duplicate About"
        )
        with self.assertRaises(ValidationError):
            second.full_clean()
        with self.assertRaises(ValidationError):
            second.save()

    def test_hotel_info_write_protection(self):
        url = reverse('hotel:hotel-info')
        for method in ['post', 'put', 'patch', 'delete']:
            client_method = getattr(self.client, method)
            res = client_method(url, {'name': 'Hacked'})
            self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ServiceTests(APITestCase):
    """
    Test suite for Service model, seeded services, and API endpoint.
    """

    def test_approved_seed_services_exist(self):
        expected_services = [
            "Wi-Fi",
            "Breakfast",
            "Parking",
            "24/7 Reception",
            "Daily Cleaning",
            "Air Conditioning"
        ]
        actual_services = list(Service.objects.order_by('sort_order').values_list('name', flat=True))
        for expected in expected_services:
            self.assertIn(expected, actual_services)
        self.assertNotIn("Laundry", actual_services)
        self.assertNotIn("Airport Transfer", actual_services)

    def test_service_list_returns_only_active_and_ordered(self):
        Service.objects.all().delete()
        Service.objects.create(name="Service B", sort_order=2, is_active=True)
        Service.objects.create(name="Service A", sort_order=1, is_active=True)
        Service.objects.create(name="Service Inactive", sort_order=0, is_active=False)

        url = reverse('hotel:service-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], "Service A")
        self.assertEqual(response.data[1]['name'], "Service B")

    def test_service_write_protection(self):
        url = reverse('hotel:service-list')
        for method in ['post', 'put', 'patch', 'delete']:
            client_method = getattr(self.client, method)
            res = client_method(url, {'name': 'Hacked'})
            self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class GalleryImageTests(APITestCase):
    """
    Test suite for GalleryImage model and API endpoint.
    """

    def test_gallery_list_returns_only_active_and_ordered(self):
        GalleryImage.objects.create(
            image=create_dummy_image("b.jpg"),
            title="Lobby View",
            sort_order=2,
            is_active=True
        )
        GalleryImage.objects.create(
            image=create_dummy_image("a.jpg"),
            title="Exterior View",
            sort_order=1,
            is_active=True
        )
        GalleryImage.objects.create(
            image=create_dummy_image("in.jpg"),
            title="Hidden Image",
            sort_order=0,
            is_active=False
        )

        url = reverse('hotel:gallery-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item['title'] for item in response.data]
        self.assertEqual(titles, ["Exterior View", "Lobby View"])
        self.assertNotIn("Hidden Image", titles)

    def test_gallery_write_protection(self):
        url = reverse('hotel:gallery-list')
        for method in ['post', 'put', 'patch', 'delete']:
            client_method = getattr(self.client, method)
            res = client_method(url, {'title': 'Hacked'})
            self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class PromotionTests(APITestCase):
    """
    Test suite for Promotion model, active date window filtering, and API endpoints.
    """

    def setUp(self):
        self.today = timezone.localdate()
        # 1. Currently active promo (active, valid window)
        self.active_promo = Promotion.objects.create(
            title="Early Bird Special",
            slug="early-bird",
            short_description="15% off when booking in advance",
            description="Detailed early bird promo description.",
            valid_from=self.today - timedelta(days=2),
            valid_until=self.today + timedelta(days=5),
            is_active=True,
            sort_order=1
        )
        # 2. Promo with null dates (open-ended active)
        self.open_promo = Promotion.objects.create(
            title="Welcome Drink Offer",
            slug="welcome-drink",
            short_description="Free welcome drink",
            description="Detailed welcome drink description.",
            valid_from=None,
            valid_until=None,
            is_active=True,
            sort_order=2
        )
        # 3. Future promo (not yet active by date)
        self.future_promo = Promotion.objects.create(
            title="Summer Holiday 2027",
            slug="summer-holiday-2027",
            short_description="Summer special",
            description="Summer details",
            valid_from=self.today + timedelta(days=10),
            valid_until=self.today + timedelta(days=30),
            is_active=True,
            sort_order=3
        )
        # 4. Expired promo (past date)
        self.expired_promo = Promotion.objects.create(
            title="Winter Deal 2023",
            slug="winter-deal-2023",
            short_description="Expired deal",
            description="Expired details",
            valid_from=self.today - timedelta(days=30),
            valid_until=self.today - timedelta(days=10),
            is_active=True,
            sort_order=4
        )
        # 5. Inactive promo (flagged is_active=False)
        self.inactive_promo = Promotion.objects.create(
            title="Draft Special",
            slug="draft-special",
            short_description="Not ready",
            description="Draft details",
            valid_from=self.today - timedelta(days=2),
            valid_until=self.today + timedelta(days=5),
            is_active=False,
            sort_order=5
        )
        self.list_url = reverse('hotel:promotion-list')

    def test_promotion_list_visibility(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        slugs = [p['slug'] for p in response.data]
        self.assertIn("early-bird", slugs)
        self.assertIn("welcome-drink", slugs)
        self.assertNotIn("summer-holiday-2027", slugs)
        self.assertNotIn("winter-deal-2023", slugs)
        self.assertNotIn("draft-special", slugs)

    def test_promotion_detail_active(self):
        url = reverse('hotel:promotion-detail', kwargs={'slug': self.active_promo.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Early Bird Special")
        self.assertEqual(response.data['description'], "Detailed early bird promo description.")

    def test_promotion_detail_404_for_inactive_future_and_expired(self):
        for promo in [self.inactive_promo, self.future_promo, self.expired_promo]:
            url = reverse('hotel:promotion-detail', kwargs={'slug': promo.slug})
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                status.HTTP_404_NOT_FOUND,
                f"Promo {promo.slug} should return 404"
            )

    def test_invalid_promotion_date_range_rejected(self):
        promo = Promotion(
            title="Invalid Dates",
            slug="invalid-dates",
            short_description="Desc",
            description="Full",
            valid_from=self.today + timedelta(days=10),
            valid_until=self.today + timedelta(days=5)
        )
        with self.assertRaises(ValidationError):
            promo.full_clean()

    def test_promotion_write_protection(self):
        for method in ['post', 'put', 'patch', 'delete']:
            client_method = getattr(self.client, method)
            res = client_method(self.list_url, {'title': 'Hacked'})
            self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
