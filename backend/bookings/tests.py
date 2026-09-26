from datetime import timedelta
from decimal import Decimal

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import IntegrityError, models, transaction
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.throttling import ScopedRateThrottle

from bookings.models import BookingRequest, BookingStatus
from bookings.views import BookingRequestCreateView
from rooms.models import Room


class BookingRequestModelTests(TestCase):
    """
    Unit tests for BookingRequest model validations, constraints, and snapshot logic.
    """

    def setUp(self):
        self.today = timezone.localdate()
        self.room = Room.objects.create(
            name="Deluxe Suite",
            slug="deluxe-suite",
            short_description="Spacious luxury suite",
            description="Full luxury suite with ocean view.",
            price_per_night=Decimal("850000.00"),
            max_adults=2,
            max_children=2,
            bed_type="1 King Bed",
            is_active=True,
        )

    def test_valid_booking_request(self):
        booking = BookingRequest(
            room=self.room,
            check_in=self.today + timedelta(days=2),
            check_out=self.today + timedelta(days=5),
            adults=2,
            children=1,
            full_name="Jane Doe",
            phone="+998901234567",
            email="jane@example.com",
            special_request="Quiet room please",
        )
        booking.full_clean()
        booking.save()

        self.assertIsNotNone(booking.id)
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.full_name, "Jane Doe")

    def test_default_status_is_new(self):
        booking = BookingRequest.objects.create(
            room=self.room,
            check_in=self.today + timedelta(days=1),
            check_out=self.today + timedelta(days=3),
            adults=1,
            children=0,
            full_name="Alice Smith",
            phone="+998901112233",
            email="alice@example.com",
        )
        self.assertEqual(booking.status, BookingStatus.NEW)

    def test_snapshots_copied_on_save(self):
        booking = BookingRequest.objects.create(
            room=self.room,
            check_in=self.today + timedelta(days=1),
            check_out=self.today + timedelta(days=4),
            adults=2,
            children=0,
            full_name="Bob Brown",
            phone="+998902223344",
            email="bob@example.com",
        )
        self.assertEqual(booking.room_name_snapshot, self.room.name)
        self.assertEqual(booking.price_per_night_snapshot, self.room.price_per_night)

    def test_past_check_in_rejected(self):
        booking = BookingRequest(
            room=self.room,
            check_in=self.today - timedelta(days=1),
            check_out=self.today + timedelta(days=2),
            adults=1,
            children=0,
            full_name="Past Guest",
            phone="+998903334455",
            email="past@example.com",
        )
        with self.assertRaises(ValidationError) as cm:
            booking.full_clean()
        self.assertIn('check_in', cm.exception.message_dict)

    def test_same_day_checkout_rejected(self):
        booking = BookingRequest(
            room=self.room,
            check_in=self.today + timedelta(days=2),
            check_out=self.today + timedelta(days=2),
            adults=1,
            children=0,
            full_name="Same Day Guest",
            phone="+998903334455",
            email="sameday@example.com",
        )
        with self.assertRaises(ValidationError) as cm:
            booking.full_clean()
        self.assertIn('check_out', cm.exception.message_dict)

    def test_checkout_before_check_in_rejected(self):
        booking = BookingRequest(
            room=self.room,
            check_in=self.today + timedelta(days=5),
            check_out=self.today + timedelta(days=2),
            adults=1,
            children=0,
            full_name="Reverse Guest",
            phone="+998903334455",
            email="reverse@example.com",
        )
        with self.assertRaises(ValidationError) as cm:
            booking.full_clean()
        self.assertIn('check_out', cm.exception.message_dict)

    def test_adults_less_than_one_rejected(self):
        booking = BookingRequest(
            room=self.room,
            check_in=self.today + timedelta(days=1),
            check_out=self.today + timedelta(days=3),
            adults=0,
            children=0,
            full_name="No Adult Guest",
            phone="+998903334455",
            email="noadult@example.com",
        )
        with self.assertRaises(ValidationError) as cm:
            booking.full_clean()
        self.assertIn('adults', cm.exception.message_dict)

    def test_children_negative_rejected(self):
        booking = BookingRequest(
            room=self.room,
            check_in=self.today + timedelta(days=1),
            check_out=self.today + timedelta(days=3),
            adults=1,
            children=-1,
            full_name="Negative Children Guest",
            phone="+998903334455",
            email="negchildren@example.com",
        )
        with self.assertRaises(ValidationError) as cm:
            booking.full_clean()
        self.assertIn('children', cm.exception.message_dict)

    def test_adults_above_room_max_rejected(self):
        booking = BookingRequest(
            room=self.room,
            check_in=self.today + timedelta(days=1),
            check_out=self.today + timedelta(days=3),
            adults=self.room.max_adults + 1,
            children=0,
            full_name="Over Capacity Adults",
            phone="+998903334455",
            email="overadults@example.com",
        )
        with self.assertRaises(ValidationError) as cm:
            booking.full_clean()
        self.assertIn('adults', cm.exception.message_dict)

    def test_children_above_room_max_rejected(self):
        booking = BookingRequest(
            room=self.room,
            check_in=self.today + timedelta(days=1),
            check_out=self.today + timedelta(days=3),
            adults=1,
            children=self.room.max_children + 1,
            full_name="Over Capacity Children",
            phone="+998903334455",
            email="overchildren@example.com",
        )
        with self.assertRaises(ValidationError) as cm:
            booking.full_clean()
        self.assertIn('children', cm.exception.message_dict)

    def test_inactive_room_rejected(self):
        self.room.is_active = False
        self.room.save()

        booking = BookingRequest(
            room=self.room,
            check_in=self.today + timedelta(days=1),
            check_out=self.today + timedelta(days=3),
            adults=1,
            children=0,
            full_name="Inactive Room Guest",
            phone="+998903334455",
            email="inactiveroom@example.com",
        )
        with self.assertRaises(ValidationError) as cm:
            booking.full_clean()
        self.assertIn('room', cm.exception.message_dict)

    def test_room_deletion_protected_when_booking_exists(self):
        BookingRequest.objects.create(
            room=self.room,
            check_in=self.today + timedelta(days=1),
            check_out=self.today + timedelta(days=3),
            adults=1,
            children=0,
            full_name="Protected Guest",
            phone="+998903334455",
            email="protected@example.com",
        )
        with self.assertRaises(models.ProtectedError):
            self.room.delete()

    def test_database_check_constraints(self):
        # Database constraint: check_out > check_in
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                BookingRequest.objects.create(
                    room=self.room,
                    check_in=self.today + timedelta(days=3),
                    check_out=self.today + timedelta(days=2),
                    adults=1,
                    children=0,
                    full_name="Constraint Violator",
                    phone="+998909998877",
                    email="violator@example.com",
                )


class BookingRequestAPITests(APITestCase):
    """
    Integration tests for POST /api/v1/bookings/ and HTTP method restrictions.
    """

    def setUp(self):
        cache.clear()
        self.today = timezone.localdate()
        self.room = Room.objects.create(
            name="Standard Twin",
            slug="standard-twin",
            short_description="Twin bed standard room",
            description="Comfortable room with two twin beds.",
            price_per_night=Decimal("450000.00"),
            max_adults=2,
            max_children=1,
            bed_type="2 Single Beds",
            is_active=True,
        )
        self.url = '/api/v1/bookings/'
        self.valid_payload = {
            'room': self.room.id,
            'check_in': (self.today + timedelta(days=2)).isoformat(),
            'check_out': (self.today + timedelta(days=5)).isoformat(),
            'adults': 2,
            'children': 1,
            'full_name': 'Sarah Connor',
            'phone': '+998901234567',
            'email': 'sarah@example.com',
            'special_request': 'High floor please',
        }

    def test_valid_booking_submission_returns_201(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookingRequest.objects.count(), 1)

        booking = BookingRequest.objects.first()
        self.assertEqual(booking.status, BookingStatus.NEW)
        self.assertEqual(booking.room_name_snapshot, self.room.name)
        self.assertEqual(booking.price_per_night_snapshot, self.room.price_per_night)

        # Check response body
        data = response.json()
        self.assertEqual(data['status'], BookingStatus.NEW)
        self.assertEqual(data['room_name_snapshot'], self.room.name)
        self.assertEqual(Decimal(data['price_per_night_snapshot']), self.room.price_per_night)
        self.assertEqual(data['full_name'], 'Sarah Connor')
        self.assertNotIn('admin_note', data)

    def test_missing_required_fields_returns_400(self):
        required_fields = ['room', 'check_in', 'check_out', 'full_name', 'phone', 'email']
        for field in required_fields:
            cache.clear()
            payload = self.valid_payload.copy()
            del payload[field]
            response = self.client.post(self.url, payload, format='json')
            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
                f"Missing field '{field}' should return 400"
            )

    def test_invalid_email_returns_400(self):
        payload = self.valid_payload.copy()
        payload['email'] = 'not-an-email'
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.json())

    def test_past_check_in_date_returns_400(self):
        payload = self.valid_payload.copy()
        payload['check_in'] = (self.today - timedelta(days=1)).isoformat()
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('check_in', response.json())

    def test_same_day_checkout_returns_400(self):
        payload = self.valid_payload.copy()
        payload['check_in'] = (self.today + timedelta(days=3)).isoformat()
        payload['check_out'] = (self.today + timedelta(days=3)).isoformat()
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('check_out', response.json())

    def test_checkout_before_check_in_returns_400(self):
        payload = self.valid_payload.copy()
        payload['check_in'] = (self.today + timedelta(days=5)).isoformat()
        payload['check_out'] = (self.today + timedelta(days=2)).isoformat()
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('check_out', response.json())

    def test_capacity_violation_adults_returns_400(self):
        payload = self.valid_payload.copy()
        payload['adults'] = self.room.max_adults + 1
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('adults', response.json())

    def test_capacity_violation_children_returns_400(self):
        payload = self.valid_payload.copy()
        payload['children'] = self.room.max_children + 1
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('children', response.json())

    def test_inactive_room_submission_rejected(self):
        self.room.is_active = False
        self.room.save()

        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('room', response.json())

    def test_public_user_cannot_list_bookings(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_public_user_cannot_get_booking_detail(self):
        booking = BookingRequest.objects.create(
            room=self.room,
            check_in=self.today + timedelta(days=1),
            check_out=self.today + timedelta(days=3),
            adults=1,
            children=0,
            full_name="Secret Guest",
            phone="+998901234567",
            email="guest@example.com",
        )
        response = self.client.get(f"{self.url}{booking.id}/")
        self.assertIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_public_user_cannot_put_booking(self):
        response = self.client.put(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_public_user_cannot_patch_booking(self):
        response = self.client.patch(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_public_user_cannot_delete_booking(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class BookingRequestSecurityTests(APITestCase):
    """
    Security tests verifying clients cannot tamper with internal or snapshot fields.
    """

    def setUp(self):
        cache.clear()
        self.today = timezone.localdate()
        self.room = Room.objects.create(
            name="Executive Suite",
            slug="executive-suite",
            short_description="Executive business suite",
            description="Full luxury executive suite.",
            price_per_night=Decimal("1200000.00"),
            max_adults=3,
            max_children=2,
            bed_type="1 King Bed + 1 Sofa",
            is_active=True,
        )
        self.url = '/api/v1/bookings/'

    def test_malicious_payload_cannot_control_status(self):
        payload = {
            'room': self.room.id,
            'check_in': (self.today + timedelta(days=2)).isoformat(),
            'check_out': (self.today + timedelta(days=4)).isoformat(),
            'adults': 2,
            'children': 0,
            'full_name': 'Attacker Bob',
            'phone': '+998900001122',
            'email': 'attacker@example.com',
            'status': 'CONFIRMED',
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        booking = BookingRequest.objects.get(email='attacker@example.com')
        self.assertEqual(booking.status, BookingStatus.NEW)
        self.assertEqual(response.json()['status'], BookingStatus.NEW)

    def test_malicious_payload_cannot_control_snapshots(self):
        payload = {
            'room': self.room.id,
            'check_in': (self.today + timedelta(days=2)).isoformat(),
            'check_out': (self.today + timedelta(days=4)).isoformat(),
            'adults': 2,
            'children': 0,
            'full_name': 'Snapshot Faker',
            'phone': '+998900001133',
            'email': 'faker@example.com',
            'room_name_snapshot': 'Cheap Closet',
            'price_per_night_snapshot': '1.00',
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        booking = BookingRequest.objects.get(email='faker@example.com')
        self.assertEqual(booking.room_name_snapshot, self.room.name)
        self.assertEqual(booking.price_per_night_snapshot, self.room.price_per_night)
        self.assertEqual(Decimal(response.json()['price_per_night_snapshot']), self.room.price_per_night)

    def test_malicious_payload_cannot_control_admin_note(self):
        payload = {
            'room': self.room.id,
            'check_in': (self.today + timedelta(days=2)).isoformat(),
            'check_out': (self.today + timedelta(days=4)).isoformat(),
            'adults': 2,
            'children': 0,
            'full_name': 'Note Injector',
            'phone': '+998900001144',
            'email': 'injector@example.com',
            'admin_note': 'Staff internal VIP discount notes',
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        booking = BookingRequest.objects.get(email='injector@example.com')
        self.assertEqual(booking.admin_note, '')
        self.assertNotIn('admin_note', response.json())


class BookingRequestDuplicateTests(APITestCase):
    """
    Tests for duplicate submission protection.
    """

    def setUp(self):
        cache.clear()
        self.today = timezone.localdate()
        self.room = Room.objects.create(
            name="Garden Bungalow",
            slug="garden-bungalow",
            short_description="Cozy garden bungalow",
            description="Peaceful bungalow surrounded by greenery.",
            price_per_night=Decimal("500000.00"),
            max_adults=2,
            max_children=1,
            bed_type="1 Queen Bed",
            is_active=True,
        )
        self.url = '/api/v1/bookings/'
        self.payload = {
            'room': self.room.id,
            'check_in': (self.today + timedelta(days=3)).isoformat(),
            'check_out': (self.today + timedelta(days=6)).isoformat(),
            'adults': 2,
            'children': 0,
            'full_name': 'David Miller',
            'phone': '+998905556677',
            'email': 'david@example.com',
            'special_request': 'Late arrival at 9 PM',
        }

    def test_rapid_duplicate_submission_does_not_create_duplicate_row(self):
        # First submission
        res1 = self.client.post(self.url, self.payload, format='json')
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookingRequest.objects.count(), 1)

        # Immediate rapid second submission (e.g. double click)
        res2 = self.client.post(self.url, self.payload, format='json')
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        # Verify no duplicate database row was created
        self.assertEqual(BookingRequest.objects.count(), 1)
        # Safe explanatory response
        data = res2.json()
        self.assertIn('already been received', data.get('detail', ''))

    def test_legitimate_separate_bookings_not_blocked(self):
        # Booking 1
        res1 = self.client.post(self.url, self.payload, format='json')
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)

        # Booking 2 with different dates
        payload2 = self.payload.copy()
        payload2['check_in'] = (self.today + timedelta(days=10)).isoformat()
        payload2['check_out'] = (self.today + timedelta(days=14)).isoformat()
        res2 = self.client.post(self.url, payload2, format='json')
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)

        # Booking 3 with different guest
        payload3 = self.payload.copy()
        payload3['email'] = 'other.guest@example.com'
        payload3['phone'] = '+998907778899'
        res3 = self.client.post(self.url, payload3, format='json')
        self.assertEqual(res3.status_code, status.HTTP_201_CREATED)

        self.assertEqual(BookingRequest.objects.count(), 3)

    def test_booking_after_duplicate_window_allowed(self):
        # First booking created 10 minutes ago
        booking = BookingRequest.objects.create(
            room=self.room,
            check_in=self.today + timedelta(days=3),
            check_out=self.today + timedelta(days=6),
            adults=2,
            children=0,
            full_name='David Miller',
            phone='+998905556677',
            email='david@example.com',
        )
        # Backdate creation time beyond 2-minute window
        BookingRequest.objects.filter(id=booking.id).update(
            created_at=timezone.now() - timedelta(minutes=10)
        )
        self.assertEqual(BookingRequest.objects.count(), 1)

        # New submission with same details after window expired
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookingRequest.objects.count(), 2)


class BookingRequestThrottleTests(APITestCase):
    """
    Tests verifying dedicated throttle configuration on booking submissions.
    """

    def setUp(self):
        cache.clear()
        self.today = timezone.localdate()
        self.room = Room.objects.create(
            name="Penthouse Suite",
            slug="penthouse-suite",
            short_description="Top-floor luxury penthouse",
            description="Panoramic view penthouse suite.",
            price_per_night=Decimal("2500000.00"),
            max_adults=4,
            max_children=2,
            bed_type="2 King Beds",
            is_active=True,
        )
        self.url = '/api/v1/bookings/'

    def test_view_throttle_configuration(self):
        from rest_framework.settings import api_settings
        self.assertEqual(BookingRequestCreateView.throttle_scope, 'booking_submission')
        self.assertIn(ScopedRateThrottle, BookingRequestCreateView.throttle_classes)
        self.assertEqual(
            api_settings.DEFAULT_THROTTLE_RATES.get('booking_submission'),
            '5/minute'
        )

    def test_booking_throttle_rate_limiting(self):
        cache.clear()
        # Configured rate is 5/minute: first 5 unique requests should succeed
        for i in range(1, 6):
            payload = {
                'room': self.room.id,
                'check_in': (self.today + timedelta(days=i + 1)).isoformat(),
                'check_out': (self.today + timedelta(days=i + 3)).isoformat(),
                'adults': 1,
                'children': 0,
                'full_name': f'Throttle Guest {i}',
                'phone': f'+99890000{i:04d}',
                'email': f'throttle{i}@example.com',
            }
            res = self.client.post(self.url, payload, format='json')
            self.assertEqual(
                res.status_code,
                status.HTTP_201_CREATED,
                f"Request {i} should be allowed within rate limit"
            )

        # 6th request exceeds 5/minute limit
        payload_overflow = {
            'room': self.room.id,
            'check_in': (self.today + timedelta(days=10)).isoformat(),
            'check_out': (self.today + timedelta(days=12)).isoformat(),
            'adults': 1,
            'children': 0,
            'full_name': 'Throttle Overflow Guest',
            'phone': '+998900009999',
            'email': 'overflow@example.com',
        }
        res_overflow = self.client.post(self.url, payload_overflow, format='json')
        self.assertEqual(
            res_overflow.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS,
            "6th request within one minute should be throttled (429)"
        )
