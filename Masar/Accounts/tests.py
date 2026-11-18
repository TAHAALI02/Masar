from django.test import TestCase
from django.urls import reverse

from .models import User

PW = "Str0ng!pass99"


class RoleAccessTests(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user("boss", password=PW, role=User.Role.FLEET_MANAGER)
        self.dispatcher = User.objects.create_user("disp", password=PW, role=User.Role.DISPATCHER)

    def status(self, user, url_name):
        self.client.force_login(user)
        return self.client.get(reverse(url_name)).status_code

    def test_both_roles_can_open_shared_pages(self):
        for user in (self.manager, self.dispatcher):
            for page in ("live_map", "alerts", "trip_history"):
                self.assertEqual(self.status(user, page), 200, f"{user.role} -> {page}")

    def test_manager_can_open_manager_pages(self):
        for page in ("reports", "user_list", "user_create"):
            self.assertEqual(self.status(self.manager, page), 200, page)

    def test_dispatcher_blocked_from_manager_pages(self):
        for page in ("reports", "user_list", "user_create"):
            self.assertEqual(self.status(self.dispatcher, page), 403, page)

    def test_dispatcher_cannot_toggle_users(self):
        self.client.force_login(self.dispatcher)
        r = self.client.post(reverse("user_toggle_active", args=[self.manager.pk]))
        self.assertEqual(r.status_code, 403)

    def test_anonymous_redirected_to_login(self):
        r = self.client.get(reverse("live_map"))
        self.assertRedirects(r, f"{reverse('login')}?next={reverse('live_map')}")

    def test_wrong_password_fails(self):
        self.client.post(reverse("login"), {"username": "boss", "password": "wrong"})
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_deactivated_user_cannot_login(self):
        self.dispatcher.is_active = False
        self.dispatcher.save()
        self.assertFalse(self.client.login(username="disp", password=PW))

    def test_manager_can_create_both_roles(self):
        self.client.force_login(self.manager)
        for name, role in (("d1", "dispatcher"), ("m2", "fleet_manager")):
            self.client.post(reverse("user_create"), {
                "username": name, "role": role,
                "password1": PW, "password2": PW,
            })
            self.assertEqual(User.objects.get(username=name).role, role)

    def test_manager_cannot_deactivate_self(self):
        self.client.force_login(self.manager)
        self.client.post(reverse("user_toggle_active", args=[self.manager.pk]))
        self.manager.refresh_from_db()
        self.assertTrue(self.manager.is_active)