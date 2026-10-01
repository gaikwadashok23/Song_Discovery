import uuid

from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserAPITestCase(APITestCase):

    def setUp(self):
        self.url = "/api/v1/users/"

        self.valid_payload = {
            "name": "Ashok Gaikwad",
            "email": "ashok@example.com",
            "preferences": {
                "genres": ["rock", "pop"],
                "artists": ["Coldplay"],
                "moods": ["happy", "relaxed"],
            },
        }

    def test_create_user(self):
        response = self.client.post(
            self.url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            User.objects.count(),
            1,
        )

        self.assertEqual(
            response.data["email"],
            "ashok@example.com",
        )

        self.assertEqual(
            response.data["name"],
            "Ashok Gaikwad",
        )

    def test_create_user_normalizes_email(self):
        payload = {
            **self.valid_payload,
            "email": "ASHOK@EXAMPLE.COM",
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["email"],
            "ashok@example.com",
        )

    def test_duplicate_email(self):
        User.objects.create_user(
            email="ashok@example.com",
            name="Existing User",
            password="test123",
        )

        response = self.client.post(
            self.url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_409_CONFLICT,
        )

        self.assertEqual(
            User.objects.count(),
            1,
        )

    def test_missing_name(self):
        payload = {
            "email": "test@example.com",
            "preferences": {},
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_empty_name(self):
        payload = {
            **self.valid_payload,
            "name": "",
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_short_name(self):
        payload = {
            **self.valid_payload,
            "name": "A",
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_invalid_preferences_type(self):
        payload = {
            **self.valid_payload,
            "preferences": {
                "genres": "rock",
            },
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_invalid_preference_key(self):
        payload = {
            **self.valid_payload,
            "preferences": {
                "languages": ["Hindi"],
            },
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_empty_preference_value(self):
        payload = {
            **self.valid_payload,
            "preferences": {
                "genres": [""],
            },
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_non_string_preference_value(self):
        payload = {
            **self.valid_payload,
            "preferences": {
                "genres": ["rock", 123],
            },
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_get_existing_user(self):
        user = User.objects.create_user(
            email="ashok@example.com",
            name="Ashok Gaikwad",
            password="test123",
        )

        response = self.client.get(
            f"{self.url}{user.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            str(user.id),
        )

    def test_get_non_existing_user(self):
        random_id = uuid.uuid4()

        response = self.client.get(
            f"{self.url}{random_id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_invalid_uuid(self):
        response = self.client.get(
            f"{self.url}invalid-uuid/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_preferences_can_be_empty(self):
        payload = {
            "name": "Test User",
            "email": "test@example.com",
            "preferences": {},
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["preferences"],
            {},
        )