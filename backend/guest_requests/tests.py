from datetime import timedelta
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.test import APITestCase
from rest_framework.throttling import ScopedRateThrottle

from guest_requests.models import CallbackRequest, ContactMessage, RequestStatus
from guest_requests.views import CallbackRequestCreateView, ContactMessageCreateView


class CallbackRequestModelTests(TestCase):
    """
    Model unit tests for CallbackRequest.
    """

    def test_valid_callback_request(self):
        req = CallbackRequest(
            full_name="Alice Smith",
            phone="+998901234567",
            preferred_time="Morning 09:00 - 12:00",
            message="Please call about presidential suite availability.",
        )
        req.full_clean()
        req.save()

        self.assertIsNotNone(req.id)
        self.assertEqual(req.status, RequestStatus.NEW)
        self.assertIn("Alice Smith", str(req))

    def test_missing_or_blank_name_rejected(self):
        req = CallbackRequest(full_name="   ", phone="+998901234567")
        with self.assertRaises(ValidationError) as cm:
            req.full_clean()
        self.assertIn('full_name', cm.exception.message_dict)

    def test_missing_or_blank_phone_rejected(self):
        req = CallbackRequest(full_name="Alice", phone="   ")
        with self.assertRaises(ValidationError) as cm:
            req.full_clean()
        self.assertIn('phone', cm.exception.message_dict)

    def test_invalid_phone_characters_rejected(self):
        req = CallbackRequest(full_name="Alice", phone="phone123abc")
        with self.assertRaises(ValidationError) as cm:
            req.full_clean()
        self.assertIn('phone', cm.exception.message_dict)

    def test_whitespace_trimmed_on_save(self):
        req = CallbackRequest.objects.create(
            full_name="  Bob White  ",
            phone="  +1 (555) 234-5678  ",
            preferred_time="  Afternoon  ",
            message="  Need info  ",
        )
        self.assertEqual(req.full_name, "Bob White")
        self.assertEqual(req.phone, "+1 (555) 234-5678")
        self.assertEqual(req.preferred_time, "Afternoon")
        self.assertEqual(req.message, "Need info")


class ContactMessageModelTests(TestCase):
    """
    Model unit tests for ContactMessage.
    """

    def test_valid_contact_message(self):
        msg = ContactMessage(
            full_name="Charlie Brown",
            email="charlie@example.com",
            phone="+998909876543",
            subject="Conference Room Booking",
            message="We would like to book the hall for 50 people.",
        )
        msg.full_clean()
        msg.save()

        self.assertIsNotNone(msg.id)
        self.assertEqual(msg.status, RequestStatus.NEW)
        self.assertIn("Conference Room", str(msg))

    def test_missing_or_blank_full_name_rejected(self):
        msg = ContactMessage(
            full_name="  ",
            email="test@example.com",
            subject="Query",
            message="Hello",
        )
        with self.assertRaises(ValidationError) as cm:
            msg.full_clean()
        self.assertIn('full_name', cm.exception.message_dict)

    def test_missing_or_blank_subject_rejected(self):
        msg = ContactMessage(
            full_name="Charlie",
            email="test@example.com",
            subject="   ",
            message="Hello",
        )
        with self.assertRaises(ValidationError) as cm:
            msg.full_clean()
        self.assertIn('subject', cm.exception.message_dict)

    def test_missing_or_blank_message_rejected(self):
        msg = ContactMessage(
            full_name="Charlie",
            email="test@example.com",
            subject="Inquiry",
            message="   ",
        )
        with self.assertRaises(ValidationError) as cm:
            msg.full_clean()
        self.assertIn('message', cm.exception.message_dict)

    def test_whitespace_trimmed_on_save(self):
        msg = ContactMessage.objects.create(
            full_name="  Diana Prince  ",
            email="diana@example.com",
            phone="  +998901112233  ",
            subject="  Spa Services  ",
            message="  Do you offer massage packages?  ",
        )
        self.assertEqual(msg.full_name, "Diana Prince")
        self.assertEqual(msg.phone, "+998901112233")
        self.assertEqual(msg.subject, "Spa Services")
        self.assertEqual(msg.message, "Do you offer massage packages?")


class CallbackRequestAPITests(APITestCase):
    """
    API tests for POST /api/v1/callback-requests/
    """

    def setUp(self):
        cache.clear()
        self.url = '/api/v1/callback-requests/'
        self.valid_payload = {
            'full_name': 'Emma Watson',
            'phone': '+998 90 123 45 67',
            'preferred_time': 'Evening after 18:00',
            'message': 'Interested in honeymoon package',
        }

    def test_valid_callback_returns_201_and_creates_record(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CallbackRequest.objects.count(), 1)

        req = CallbackRequest.objects.first()
        self.assertEqual(req.status, RequestStatus.NEW)
        self.assertEqual(req.full_name, 'Emma Watson')
        self.assertEqual(req.phone, '+998 90 123 45 67')

        data = response.json()
        self.assertEqual(data['status'], RequestStatus.NEW)
        self.assertIn('received', data.get('detail', ''))
        self.assertNotIn('admin_note', data)

    def test_missing_name_rejected(self):
        payload = self.valid_payload.copy()
        del payload['full_name']
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('full_name', response.json())

    def test_missing_phone_rejected(self):
        payload = self.valid_payload.copy()
        del payload['phone']
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone', response.json())

    def test_whitespace_only_name_rejected(self):
        payload = self.valid_payload.copy()
        payload['full_name'] = '   '
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('full_name', response.json())

    def test_whitespace_only_phone_rejected(self):
        payload = self.valid_payload.copy()
        payload['phone'] = '   '
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone', response.json())

    def test_invalid_phone_format_rejected(self):
        payload = self.valid_payload.copy()
        payload['phone'] = 'invalid-phone-abc'
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone', response.json())

    def test_status_manipulation_blocked(self):
        payload = self.valid_payload.copy()
        payload['status'] = 'CLOSED'
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        req = CallbackRequest.objects.first()
        self.assertEqual(req.status, RequestStatus.NEW)
        self.assertEqual(response.json()['status'], RequestStatus.NEW)

    def test_admin_note_manipulation_blocked(self):
        payload = self.valid_payload.copy()
        payload['admin_note'] = 'VIP client - give discount'
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        req = CallbackRequest.objects.first()
        self.assertEqual(req.admin_note, '')
        self.assertNotIn('admin_note', response.json())

    def test_get_list_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_detail_route_not_exposed(self):
        req = CallbackRequest.objects.create(full_name="Secret", phone="+998901112233")
        response = self.client.get(f"{self.url}{req.id}/")
        self.assertIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_put_patch_delete_not_allowed(self):
        self.assertEqual(self.client.put(self.url, self.valid_payload).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.patch(self.url, self.valid_payload).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.delete(self.url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_duplicate_callback_prevented(self):
        # 1st request succeeds
        res1 = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CallbackRequest.objects.count(), 1)

        # 2nd identical request is recognized as duplicate
        res2 = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(CallbackRequest.objects.count(), 1)
        self.assertIn('already been received', res2.json().get('detail', ''))

    def test_legitimate_different_callback_allowed(self):
        res1 = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)

        payload2 = self.valid_payload.copy()
        payload2['phone'] = '+998907778899'
        payload2['full_name'] = 'Different Guest'
        res2 = self.client.post(self.url, payload2, format='json')
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CallbackRequest.objects.count(), 2)

    def test_honeypot_submission_rejected_and_not_created(self):
        payload = self.valid_payload.copy()
        payload['website'] = 'http://spam-bot-link.com'
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CallbackRequest.objects.count(), 0)


class ContactMessageAPITests(APITestCase):
    """
    API tests for POST /api/v1/contact-messages/
    """

    def setUp(self):
        cache.clear()
        self.url = '/api/v1/contact-messages/'
        self.valid_payload = {
            'full_name': 'George Clark',
            'email': 'george@example.com',
            'phone': '+998901234567',
            'subject': 'Airport Transfer Query',
            'message': 'Do you offer pickup service from Tashkent International Airport?',
        }

    def test_valid_contact_message_returns_201_and_creates_record(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactMessage.objects.count(), 1)

        msg = ContactMessage.objects.first()
        self.assertEqual(msg.status, RequestStatus.NEW)
        self.assertEqual(msg.full_name, 'George Clark')

        data = response.json()
        self.assertEqual(data['status'], RequestStatus.NEW)
        self.assertIn('received', data.get('detail', ''))
        self.assertNotIn('admin_note', data)

    def test_invalid_email_rejected(self):
        payload = self.valid_payload.copy()
        payload['email'] = 'not-valid-email'
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.json())

    def test_missing_subject_rejected(self):
        payload = self.valid_payload.copy()
        del payload['subject']
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('subject', response.json())

    def test_blank_whitespace_subject_rejected(self):
        payload = self.valid_payload.copy()
        payload['subject'] = '   '
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('subject', response.json())

    def test_missing_message_rejected(self):
        payload = self.valid_payload.copy()
        del payload['message']
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.json())

    def test_blank_whitespace_message_rejected(self):
        payload = self.valid_payload.copy()
        payload['message'] = '   '
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.json())

    def test_status_manipulation_blocked(self):
        payload = self.valid_payload.copy()
        payload['status'] = 'CLOSED'
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        msg = ContactMessage.objects.first()
        self.assertEqual(msg.status, RequestStatus.NEW)
        self.assertEqual(response.json()['status'], RequestStatus.NEW)

    def test_admin_note_manipulation_blocked(self):
        payload = self.valid_payload.copy()
        payload['admin_note'] = 'Hacked internal notes'
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        msg = ContactMessage.objects.first()
        self.assertEqual(msg.admin_note, '')
        self.assertNotIn('admin_note', response.json())

    def test_get_list_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_detail_route_not_exposed(self):
        msg = ContactMessage.objects.create(
            full_name="Secret",
            email="sec@example.com",
            subject="Test",
            message="Content",
        )
        response = self.client.get(f"{self.url}{msg.id}/")
        self.assertIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_put_patch_delete_not_allowed(self):
        self.assertEqual(self.client.put(self.url, self.valid_payload).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.patch(self.url, self.valid_payload).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.delete(self.url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_duplicate_message_prevented(self):
        res1 = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactMessage.objects.count(), 1)

        res2 = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertIn('already been received', res2.json().get('detail', ''))

    def test_legitimate_separate_message_allowed(self):
        res1 = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)

        payload2 = self.valid_payload.copy()
        payload2['subject'] = 'Different Subject: Laundry Services'
        res2 = self.client.post(self.url, payload2, format='json')
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactMessage.objects.count(), 2)

    def test_honeypot_submission_rejected_and_not_created(self):
        payload = self.valid_payload.copy()
        payload['website'] = 'http://spam-payload.xyz'
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ContactMessage.objects.count(), 0)


class GuestRequestsThrottlingTests(APITestCase):
    """
    Throttle configuration and rate limit tests for guest requests.
    """

    def setUp(self):
        cache.clear()

    def test_throttle_scopes_and_classes(self):
        self.assertEqual(CallbackRequestCreateView.throttle_scope, 'callback_submission')
        self.assertIn(ScopedRateThrottle, CallbackRequestCreateView.throttle_classes)
        self.assertEqual(
            api_settings.DEFAULT_THROTTLE_RATES.get('callback_submission'),
            '5/minute'
        )

        self.assertEqual(ContactMessageCreateView.throttle_scope, 'contact_submission')
        self.assertIn(ScopedRateThrottle, ContactMessageCreateView.throttle_classes)
        self.assertEqual(
            api_settings.DEFAULT_THROTTLE_RATES.get('contact_submission'),
            '5/minute'
        )

    def test_callback_throttle_rate_limiting(self):
        cache.clear()
        url = '/api/v1/callback-requests/'
        # 5 allowed, 6th throttled
        for i in range(1, 6):
            payload = {
                'full_name': f'Throttle Guest {i}',
                'phone': f'+99890111{i:04d}',
                'message': f'Message {i}',
            }
            res = self.client.post(url, payload, format='json')
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        overflow_payload = {
            'full_name': 'Overflow Guest',
            'phone': '+998909999999',
            'message': 'Overflow message',
        }
        res_overflow = self.client.post(url, overflow_payload, format='json')
        self.assertEqual(res_overflow.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_contact_throttle_rate_limiting(self):
        cache.clear()
        url = '/api/v1/contact-messages/'
        # 5 allowed, 6th throttled
        for i in range(1, 6):
            payload = {
                'full_name': f'Throttle Guest {i}',
                'email': f'throttle{i}@example.com',
                'subject': f'Subject {i}',
                'message': f'Message body {i}',
            }
            res = self.client.post(url, payload, format='json')
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        overflow_payload = {
            'full_name': 'Overflow Guest',
            'email': 'overflow@example.com',
            'subject': 'Overflow Subject',
            'message': 'Overflow body',
        }
        res_overflow = self.client.post(url, overflow_payload, format='json')
        self.assertEqual(res_overflow.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
