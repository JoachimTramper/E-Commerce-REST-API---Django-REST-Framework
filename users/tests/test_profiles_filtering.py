from datetime import timedelta

import pytest
from django.urls import reverse
from rest_framework import status

from users.models import CustomerProfile


@pytest.mark.django_db
class TestProfileFilters:
    def test_filter_profiles_by_phone_number_contains(self, admin_client, user_factory):
        # create two users with different phone numbers
        user1 = user_factory(email="p1@example.com", username="p1")
        CustomerProfile.objects.create(user=user1, phone_number="0611234567")

        user2 = user_factory(email="p2@example.com", username="p2")
        CustomerProfile.objects.create(user=user2, phone_number="0629998888")

        url = reverse("users:profiles-list") + "?phone_number__icontains=06112"
        resp = admin_client.get(url)
        assert resp.status_code == status.HTTP_200_OK

        results = resp.json()["results"]
        phone_numbers = {p["phone_number"] for p in results}

        # only the profile with phone_number containing "06112" should be returned
        assert "0611234567" in phone_numbers
        assert "0629998888" not in phone_numbers

    def test_filter_profiles_by_user_exact(self, admin_client, user_factory):
        user1 = user_factory(email="x@example.com", username="x")
        CustomerProfile.objects.create(user=user1, phone_number="0610000000")

        user2 = user_factory(email="y@example.com", username="y")
        CustomerProfile.objects.create(user=user2, phone_number="0620000000")

        url = reverse("users:profiles-list") + f"?user={user2.id}"
        resp = admin_client.get(url)
        assert resp.status_code == status.HTTP_200_OK

        results = resp.json()["results"]
        # exactly one profile (that of user2) should be returned
        assert len(results) == 1
        assert results[0]["user"] == user2.id

    def test_order_profiles_by_user_date_joined(
        self, admin_client, user_factory, freeze_time, monkeypatch
    ):
        # create a profile at the frozen time
        user1 = user_factory(username="old", email="old@example.com")
        profile1 = CustomerProfile.objects.create(user=user1, phone_number="0611111111")

        # advance time by 1 day and create a second profile
        later = freeze_time + timedelta(days=1)
        monkeypatch.setattr("django.utils.timezone.now", lambda: later)
        user2 = user_factory(username="new", email="new@example.com")
        profile2 = CustomerProfile.objects.create(user=user2, phone_number="0622222222")

        # restore original time function
        monkeypatch.setattr("django.utils.timezone.now", lambda: freeze_time)

        url = reverse("users:profiles-list") + "?ordering=user__date_joined"
        resp = admin_client.get(url)
        assert resp.status_code == status.HTTP_200_OK

        results = resp.json()["results"]
        # first result must be the older profile, then the newer one
        assert results[0]["id"] == profile1.id
        assert results[1]["id"] == profile2.id
