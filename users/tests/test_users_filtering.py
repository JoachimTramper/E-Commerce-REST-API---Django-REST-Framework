from datetime import timedelta

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUserSearchAndOrdering:
    def test_search_users_by_username(self, admin_client, user_factory):
        user_factory(username="alice", email="a@e.com")
        user_factory(username="bob", email="b@e.com")

        url = reverse("users:users-list") + "?search=ali"
        resp = admin_client.get(url)
        assert resp.status_code == status.HTTP_200_OK

        results = resp.json()["results"]
        assert any(u["username"] == "alice" for u in results)
        assert all("ali" in u["username"] for u in results)

    def test_order_users_by_date_joined_descending(
        self, admin_client, user_factory, freeze_time, monkeypatch
    ):
        # create one user at the current time
        user_factory(username="first")

        # move time forward by one day and create another user
        later = freeze_time + timedelta(days=1)
        monkeypatch.setattr("django.utils.timezone.now", lambda: later)
        user_factory(username="second")

        # restore time to the original time for the rest of the test
        monkeypatch.setattr("django.utils.timezone.now", lambda: freeze_time)

        url = reverse("users:users-list") + "?ordering=-date_joined"
        resp = admin_client.get(url)
        assert resp.status_code == status.HTTP_200_OK

        results = resp.json()["results"]
        assert results[0]["username"] == "second"
        assert results[1]["username"] == "first"


@pytest.mark.django_db
class TestUserFieldFilters:
    @pytest.fixture(autouse=True)
    def init_users(self, user_factory):
        # inactive and active user
        self.active_user = user_factory(
            is_active=True, email="a@ex.com", username="active"
        )
        self.inactive_user = user_factory(
            is_active=False, email="b@ex.com", username="inactive"
        )

        # staff and non-staff user
        self.staff_user = user_factory(
            is_staff=True, email="s@ex.com", username="staff"
        )
        self.normal_user = user_factory(
            is_staff=False, email="n@ex.com", username="normal"
        )

        self.url = reverse("users:users-list")

    def test_filter_users_by_is_active_false(self, admin_client):
        resp = admin_client.get(f"{self.url}?is_active=False")
        assert resp.status_code == status.HTTP_200_OK

        returned_ids = {u["id"] for u in resp.json()["results"]}
        assert self.inactive_user.id in returned_ids
        assert self.active_user.id not in returned_ids

    def test_filter_users_by_is_staff_true(self, admin_client):
        resp = admin_client.get(f"{self.url}?is_staff=True")
        assert resp.status_code == status.HTTP_200_OK

        returned_ids = {u["id"] for u in resp.json()["results"]}
        assert self.staff_user.id in returned_ids
        assert self.normal_user.id not in returned_ids
