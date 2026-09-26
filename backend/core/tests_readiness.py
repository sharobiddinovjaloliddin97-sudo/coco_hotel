from datetime import timedelta
from unittest.mock import patch
from django.test import TestCase, SimpleTestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient
from rooms.models import Room
from bookings.models import BookingRequest
from core.storage import SupabaseMediaStorage


class MediaURLTests(SimpleTestCase):
    @override_settings(SUPABASE_PUBLIC_MEDIA_URL='https://example.supabase.co/storage/v1/object/public/coco-media')
    def test_public_url_escapes_names_without_signing_or_credentials(self):
        storage = SupabaseMediaStorage(access_key='test', secret_key='test', bucket_name='coco-media')
        self.assertEqual(storage.url('rooms/my photo.jpg'), 'https://example.supabase.co/storage/v1/object/public/coco-media/rooms/my%20photo.jpg')


class BookingReadinessTests(TestCase):
    def setUp(self):
        from django.core.cache import cache
        cache.clear()
        self.room = Room.objects.create(name='Garden', slug='garden', price_per_night=500000, max_adults=2, max_children=0)
        self.payload = dict(room=self.room.id, check_in=str(timezone.localdate() + timedelta(days=1)), check_out=str(timezone.localdate() + timedelta(days=2)), adults=1, children=0, full_name='Guest', phone='+998901234567', email='guest@example.com')
        self.client = APIClient()

    def test_honeypot_rejected_without_saving(self):
        response = self.client.post('/api/v1/bookings/', {**self.payload, 'website': 'spam.test'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(BookingRequest.objects.exists())

    def test_invalid_phone_rejected(self):
        response = self.client.post('/api/v1/bookings/', {**self.payload, 'phone': 'abcdefghi'}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_staff_can_complete_past_booking_for_inactive_room(self):
        response = self.client.post('/api/v1/bookings/', self.payload, format='json')
        self.assertEqual(response.status_code, 201)
        booking = BookingRequest.objects.get()
        self.room.is_active = False
        self.room.save()
        booking.room = self.room
        booking.status = 'COMPLETED'
        with patch('bookings.models.timezone.localdate', return_value=timezone.localdate() + timedelta(days=10)):
            booking.full_clean()
            booking.save()
        self.assertEqual(BookingRequest.objects.get().status, 'COMPLETED')

    def test_public_cannot_list_or_change_saved_requests(self):
        response = self.client.post('/api/v1/bookings/', self.payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.client.get('/api/v1/bookings/').status_code, 405)
        self.assertEqual(self.client.patch(f"/api/v1/bookings/{response.data['id']}/", {'status': 'CONFIRMED'}).status_code, 404)
