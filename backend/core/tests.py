import io
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from bookings.models import BookingRequest, BookingStatus
from guest_requests.models import CallbackRequest, ContactMessage, RequestStatus
from rooms.models import Amenity, Room

User = get_user_model()


class HealthCheckTests(APITestCase):
    """
    Automated test suite for the /api/v1/health/ endpoint.
    """

    def setUp(self):
        self.health_url = reverse('core:health-check')

    def test_health_check_returns_200(self):
        """Verify GET /api/v1/health/ returns HTTP 200."""
        response = self.client.get(self.health_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health_check_response_body(self):
        """Verify JSON response payload is exact: {'status': 'ok'}."""
        response = self.client.get(self.health_url)
        self.assertEqual(response.data, {"status": "ok"})

    def test_health_check_accessible_without_auth(self):
        """Verify endpoint is publicly accessible without authentication."""
        self.client.credentials()
        response = self.client.get(self.health_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"status": "ok"})

    def test_health_check_post_method_not_allowed(self):
        """Verify POST method returns 405 Method Not Allowed."""
        response = self.client.post(self.health_url, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_health_check_put_method_not_allowed(self):
        """Verify PUT method returns 405 Method Not Allowed."""
        response = self.client.put(self.health_url, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_health_check_delete_method_not_allowed(self):
        """Verify DELETE method returns 405 Method Not Allowed."""
        response = self.client.delete(self.health_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_health_check_direct_path(self):
        """Verify direct path /api/v1/health/ resolves and responds with 200."""
        response = self.client.get('/api/v1/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"status": "ok"})


class GroupCreationCommandTests(TestCase):
    """
    Tests for the setup_hotel_groups management command.
    """

    def test_setup_hotel_groups_creates_groups(self):
        out = io.StringIO()
        call_command('setup_hotel_groups', stdout=out)

        self.assertTrue(Group.objects.filter(name='Receptionist').exists())
        self.assertTrue(Group.objects.filter(name='Manager').exists())

        recep_group = Group.objects.get(name='Receptionist')
        manager_group = Group.objects.get(name='Manager')

        self.assertEqual(recep_group.permissions.count(), 8)
        self.assertEqual(manager_group.permissions.count(), 32)

    def test_setup_hotel_groups_is_idempotent(self):
        out = io.StringIO()
        call_command('setup_hotel_groups', stdout=out)
        call_command('setup_hotel_groups', stdout=out)

        self.assertEqual(Group.objects.filter(name='Receptionist').count(), 1)
        self.assertEqual(Group.objects.filter(name='Manager').count(), 1)

    def test_setup_hotel_groups_deterministic_permissions(self):
        call_command('setup_hotel_groups')
        recep_group = Group.objects.get(name='Receptionist')
        manager_group = Group.objects.get(name='Manager')

        # Add an unintended permission manually to simulate drift
        unintended_perm = Permission.objects.get(codename='delete_bookingrequest')
        recep_group.permissions.add(unintended_perm)
        self.assertEqual(recep_group.permissions.count(), 9)

        # Re-running the command must restore the exact intended permission set
        call_command('setup_hotel_groups')
        recep_group.refresh_from_db()
        self.assertEqual(recep_group.permissions.count(), 8)
        self.assertFalse(recep_group.permissions.filter(codename='delete_bookingrequest').exists())


class StaffRolePermissionsTests(TestCase):
    """
    Tests verifying permission boundaries for Receptionist, Manager, and Superuser.
    """

    @classmethod
    def setUpTestData(cls):
        call_command('setup_hotel_groups')
        cls.recep_group = Group.objects.get(name='Receptionist')
        cls.manager_group = Group.objects.get(name='Manager')

    def setUp(self):
        self.receptionist_user = User.objects.create_user(
            username='receptionist_test',
            password='password123',
            is_staff=True,
            is_superuser=False,
        )
        self.receptionist_user.groups.add(self.recep_group)

        self.manager_user = User.objects.create_user(
            username='manager_test',
            password='password123',
            is_staff=True,
            is_superuser=False,
        )
        self.manager_user.groups.add(self.manager_group)

        self.super_user = User.objects.create_superuser(
            username='super_test',
            password='password123',
        )

    def test_receptionist_can_view_and_change_operational_models(self):
        u = self.receptionist_user
        # Booking requests
        self.assertTrue(u.has_perm('bookings.view_bookingrequest'))
        self.assertTrue(u.has_perm('bookings.change_bookingrequest'))
        # Callback requests
        self.assertTrue(u.has_perm('guest_requests.view_callbackrequest'))
        self.assertTrue(u.has_perm('guest_requests.change_callbackrequest'))
        # Contact messages
        self.assertTrue(u.has_perm('guest_requests.view_contactmessage'))
        self.assertTrue(u.has_perm('guest_requests.change_contactmessage'))
        # Read-only reference for rooms and amenities
        self.assertTrue(u.has_perm('rooms.view_room'))
        self.assertTrue(u.has_perm('rooms.view_amenity'))

    def test_receptionist_cannot_delete_operational_models(self):
        u = self.receptionist_user
        self.assertFalse(u.has_perm('bookings.delete_bookingrequest'))
        self.assertFalse(u.has_perm('guest_requests.delete_callbackrequest'))
        self.assertFalse(u.has_perm('guest_requests.delete_contactmessage'))

    def test_receptionist_cannot_manage_content_or_auth(self):
        u = self.receptionist_user
        # Rooms and images
        self.assertFalse(u.has_perm('rooms.add_room'))
        self.assertFalse(u.has_perm('rooms.change_room'))
        self.assertFalse(u.has_perm('rooms.delete_room'))
        self.assertFalse(u.has_perm('rooms.view_roomimage'))
        self.assertFalse(u.has_perm('rooms.add_roomimage'))
        self.assertFalse(u.has_perm('rooms.change_amenity'))
        # Hotel content
        self.assertFalse(u.has_perm('hotel.view_hotelinformation'))
        self.assertFalse(u.has_perm('hotel.view_service'))
        self.assertFalse(u.has_perm('hotel.view_galleryimage'))
        self.assertFalse(u.has_perm('hotel.view_promotion'))
        # Auth system
        self.assertFalse(u.has_perm('auth.view_user'))
        self.assertFalse(u.has_perm('auth.change_user'))
        self.assertFalse(u.has_perm('auth.view_group'))
        self.assertFalse(u.has_perm('auth.view_permission'))

    def test_manager_can_manage_content_and_operational_models(self):
        u = self.manager_user
        # Operational
        self.assertTrue(u.has_perm('bookings.view_bookingrequest'))
        self.assertTrue(u.has_perm('bookings.change_bookingrequest'))
        self.assertTrue(u.has_perm('guest_requests.view_callbackrequest'))
        self.assertTrue(u.has_perm('guest_requests.change_callbackrequest'))
        self.assertTrue(u.has_perm('guest_requests.view_contactmessage'))
        self.assertTrue(u.has_perm('guest_requests.change_contactmessage'))
        # Rooms
        self.assertTrue(u.has_perm('rooms.view_room'))
        self.assertTrue(u.has_perm('rooms.add_room'))
        self.assertTrue(u.has_perm('rooms.change_room'))
        # Room images
        self.assertTrue(u.has_perm('rooms.view_roomimage'))
        self.assertTrue(u.has_perm('rooms.add_roomimage'))
        self.assertTrue(u.has_perm('rooms.change_roomimage'))
        self.assertTrue(u.has_perm('rooms.delete_roomimage'))
        # Amenities
        self.assertTrue(u.has_perm('rooms.view_amenity'))
        self.assertTrue(u.has_perm('rooms.add_amenity'))
        self.assertTrue(u.has_perm('rooms.change_amenity'))
        self.assertTrue(u.has_perm('rooms.delete_amenity'))
        # Hotel info
        self.assertTrue(u.has_perm('hotel.view_hotelinformation'))
        self.assertTrue(u.has_perm('hotel.change_hotelinformation'))
        # Services
        self.assertTrue(u.has_perm('hotel.view_service'))
        self.assertTrue(u.has_perm('hotel.add_service'))
        self.assertTrue(u.has_perm('hotel.change_service'))
        self.assertTrue(u.has_perm('hotel.delete_service'))
        # Gallery
        self.assertTrue(u.has_perm('hotel.view_galleryimage'))
        self.assertTrue(u.has_perm('hotel.add_galleryimage'))
        self.assertTrue(u.has_perm('hotel.delete_galleryimage'))
        # Promotions
        self.assertTrue(u.has_perm('hotel.view_promotion'))
        self.assertTrue(u.has_perm('hotel.add_promotion'))
        self.assertTrue(u.has_perm('hotel.change_promotion'))
        self.assertTrue(u.has_perm('hotel.delete_promotion'))

    def test_manager_cannot_delete_operational_records(self):
        u = self.manager_user
        self.assertFalse(u.has_perm('bookings.delete_bookingrequest'))
        self.assertFalse(u.has_perm('guest_requests.delete_callbackrequest'))
        self.assertFalse(u.has_perm('guest_requests.delete_contactmessage'))

    def test_manager_cannot_manage_auth(self):
        u = self.manager_user
        self.assertFalse(u.has_perm('auth.view_user'))
        self.assertFalse(u.has_perm('auth.add_user'))
        self.assertFalse(u.has_perm('auth.change_user'))
        self.assertFalse(u.has_perm('auth.delete_user'))
        self.assertFalse(u.has_perm('auth.view_group'))
        self.assertFalse(u.has_perm('auth.add_group'))
        self.assertFalse(u.has_perm('auth.change_group'))
        self.assertFalse(u.has_perm('auth.delete_group'))

    def test_superuser_retains_all_permissions(self):
        u = self.super_user
        self.assertTrue(u.has_perm('bookings.delete_bookingrequest'))
        self.assertTrue(u.has_perm('rooms.delete_room'))
        self.assertTrue(u.has_perm('auth.view_user'))
        self.assertTrue(u.has_perm('auth.add_user'))


class AdminPageAccessTests(TestCase):
    """
    HTTP level tests checking Django Admin access for Receptionist, Manager, and non-staff.
    """

    @classmethod
    def setUpTestData(cls):
        call_command('setup_hotel_groups')
        cls.recep_group = Group.objects.get(name='Receptionist')
        cls.manager_group = Group.objects.get(name='Manager')

    def setUp(self):
        self.client = Client()
        self.recep_user = User.objects.create_user(
            username='recep_admin_test',
            password='password123',
            is_staff=True,
        )
        self.recep_user.groups.add(self.recep_group)

        self.manager_user = User.objects.create_user(
            username='mgr_admin_test',
            password='password123',
            is_staff=True,
        )
        self.manager_user.groups.add(self.manager_group)

        self.regular_user = User.objects.create_user(
            username='regular_test',
            password='password123',
            is_staff=False,
        )

    def test_non_staff_redirected_from_admin(self):
        self.client.login(username='regular_test', password='password123')
        response = self.client.get('/admin/')
        # Non-staff users must be redirected to admin login
        self.assertEqual(response.status_code, 302)

    def test_receptionist_admin_page_access(self):
        self.client.login(username='recep_admin_test', password='password123')

        # Admin index succeeds
        res = self.client.get('/admin/')
        self.assertEqual(res.status_code, 200)

        # Operational changelists accessible
        self.assertEqual(self.client.get('/admin/bookings/bookingrequest/').status_code, 200)
        self.assertEqual(self.client.get('/admin/guest_requests/callbackrequest/').status_code, 200)
        self.assertEqual(self.client.get('/admin/guest_requests/contactmessage/').status_code, 200)

        # Read-only room changelist accessible
        self.assertEqual(self.client.get('/admin/rooms/room/').status_code, 200)

        # Editing rooms forbidden (403)
        self.assertEqual(self.client.get('/admin/rooms/room/add/').status_code, 403)

        # Hotel services forbidden (403)
        self.assertEqual(self.client.get('/admin/hotel/service/').status_code, 403)

        # Auth user management forbidden (403)
        self.assertEqual(self.client.get('/admin/auth/user/').status_code, 403)

    def test_manager_admin_page_access(self):
        self.client.login(username='mgr_admin_test', password='password123')

        # Admin index succeeds
        self.assertEqual(self.client.get('/admin/').status_code, 200)

        # Operational changelists accessible
        self.assertEqual(self.client.get('/admin/bookings/bookingrequest/').status_code, 200)

        # Content management accessible
        self.assertEqual(self.client.get('/admin/rooms/room/').status_code, 200)
        self.assertEqual(self.client.get('/admin/rooms/room/add/').status_code, 200)
        self.assertEqual(self.client.get('/admin/hotel/service/').status_code, 200)

        # Auth user management forbidden (403)
        self.assertEqual(self.client.get('/admin/auth/user/').status_code, 403)


class AdminActionsTests(TestCase):
    """
    Tests for operational admin actions on BookingRequest, CallbackRequest, and ContactMessage.
    """

    def setUp(self):
        self.room = Room.objects.create(
            name="Action Test Room",
            slug="action-test-room",
            short_description="Short",
            description="Full description",
            price_per_night=Decimal("500000.00"),
            max_adults=2,
            max_children=1,
            bed_type="1 Bed",
            is_active=True,
        )

    def test_booking_request_admin_actions(self):
        booking = BookingRequest.objects.create(
            room=self.room,
            check_in=timezone.localdate(),
            check_out=timezone.localdate() + timezone.timedelta(days=2),
            adults=1,
            children=0,
            full_name="Action Guest",
            phone="+998901234567",
            email="action@example.com",
            status=BookingStatus.NEW,
        )
        from bookings.admin import BookingRequestAdmin
        from django.contrib.admin.sites import AdminSite
        from django.test import RequestFactory
        from django.contrib.sessions.middleware import SessionMiddleware
        from django.contrib.messages.middleware import MessageMiddleware

        rf = RequestFactory()
        request = rf.get('/admin/')
        SessionMiddleware(lambda req: None).process_request(request)
        MessageMiddleware(lambda req: None).process_request(request)

        admin_instance = BookingRequestAdmin(BookingRequest, AdminSite())

        # Test mark_as_contacted
        qs = BookingRequest.objects.filter(id=booking.id)
        admin_instance.mark_as_contacted(request, qs)
        booking.refresh_from_db()
        self.assertEqual(booking.status, BookingStatus.CONTACTED)

        # Test mark_as_confirmed
        admin_instance.mark_as_confirmed(request, qs)
        booking.refresh_from_db()
        self.assertEqual(booking.status, BookingStatus.CONFIRMED)

        # Test mark_as_completed
        admin_instance.mark_as_completed(request, qs)
        booking.refresh_from_db()
        self.assertEqual(booking.status, BookingStatus.COMPLETED)

        # Test mark_as_cancelled
        admin_instance.mark_as_cancelled(request, qs)
        booking.refresh_from_db()
        self.assertEqual(booking.status, BookingStatus.CANCELLED)

    def test_callback_and_contact_admin_actions(self):
        cb = CallbackRequest.objects.create(
            full_name="CB Guest",
            phone="+998901112233",
            status=RequestStatus.NEW,
        )
        cm = ContactMessage.objects.create(
            full_name="CM Guest",
            email="cm@example.com",
            subject="Subj",
            message="Msg",
            status=RequestStatus.NEW,
        )

        from guest_requests.admin import CallbackRequestAdmin, ContactMessageAdmin
        from django.contrib.admin.sites import AdminSite
        from django.test import RequestFactory
        from django.contrib.sessions.middleware import SessionMiddleware
        from django.contrib.messages.middleware import MessageMiddleware

        rf = RequestFactory()
        request = rf.get('/admin/')
        SessionMiddleware(lambda req: None).process_request(request)
        MessageMiddleware(lambda req: None).process_request(request)

        cb_admin = CallbackRequestAdmin(CallbackRequest, AdminSite())
        cm_admin = ContactMessageAdmin(ContactMessage, AdminSite())

        # Callback actions
        cb_qs = CallbackRequest.objects.filter(id=cb.id)
        cb_admin.mark_as_contacted(request, cb_qs)
        cb.refresh_from_db()
        self.assertEqual(cb.status, RequestStatus.CONTACTED)

        cb_admin.mark_as_closed(request, cb_qs)
        cb.refresh_from_db()
        self.assertEqual(cb.status, RequestStatus.CLOSED)

        # Contact actions
        cm_qs = ContactMessage.objects.filter(id=cm.id)
        cm_admin.mark_as_contacted(request, cm_qs)
        cm.refresh_from_db()
        self.assertEqual(cm.status, RequestStatus.CONTACTED)

        cm_admin.mark_as_closed(request, cm_qs)
        cm.refresh_from_db()
        self.assertEqual(cm.status, RequestStatus.CLOSED)
