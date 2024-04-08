from django.test import TestCase
from rest_framework.test import APIClient
from custom_auth.models import CustomUser as User
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreateTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_user(self):
        response = self.client.post(
            "/api/users/",
            {
                "email": "test@gmail.com",
                "password": "password",
                "first_name": "John",
                "last_name": "Doe",
            },
        )
        self.assertTrue(User.objects.filter(email="test@gmail.com").exists())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["email"], "test@gmail.com")
        self.assertEqual(response.json()["first_name"], "John")
        self.assertEqual(response.json()["last_name"], "Doe")
        self.assertTrue("id" in response.json())
        self.assertTrue("referral_code" in response.json())
        self.assertIsNone(response.json()["referred_by"])
        self.assertTrue("password" not in response.json())

    def test_create_user_invalid_data(self):
        response = self.client.post(
            "/api/users/",
            {
                "email": "test1@gmail.com",
                "password": "password",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email="test1@gmail.com").exists())

    def test_create_user_with_referred_by(self):
        user = User.objects.create_user(
            email="test@b.com",
            password="password",
            first_name="John",
        )
        response = self.client.post(
            "/api/users/",
            {
                "email": "test@k.com",
                "password": "password",
                "first_name": "Jane",
                "referred_by": user.referral_code,
            },
        )
        self.assertTrue(User.objects.filter(email="test@k.com").exists())
        self.assertTrue(
            User.objects.filter(
                referral_code=response.json().get("referred_by")
            ).exists()
        )

    def test_create_user_with_invalid_referred_by(self):
        response = self.client.post(
            "/api/users/",
            {
                "email": "test@m.com",
                "password": "password",
                "first_name": "Jane",
                "referred_by": "invalid",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email="test@m.com").exists())

    def test_current_user(self):
        user = User.objects.create_user(
            email="test@a.com",
            password="password",
            first_name="John",
        )
        token = RefreshToken.for_user(user)
        response = self.client.get(
            "/api/users/me/", HTTP_AUTHORIZATION=f"Bearer {token.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], user.email)
        self.assertTrue("date_joined" in response.json())


class UserListTests(TestCase):
    referred_user_data = [
        {
            "email": "test4@gmail.com",
            "password": "password",
            "first_name": "Jane",
        },
        {
            "email": "test5@gmail.com",
            "password": "password",
            "first_name": "Jane",
        },
        {
            "email": "test6@gmail.com",
            "password": "password",
            "first_name": "Jane",
        },
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test3@gmail.com",
            password="password",
            first_name="John",
            last_name="Doe",
        )
        for user in self.referred_user_data:
            User.objects.create_user(**user, referred_by=self.user.referral_code)

    def test_list_users_with_referred_users(self):
        token = RefreshToken.for_user(self.user)
        response = self.client.get(
            "/api/users/referred/", HTTP_AUTHORIZATION=f"Bearer {token.access_token}"
        )
        results = response.json().get("results")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(results), 3)
        self.assertTrue("date_joined" in results[0])
