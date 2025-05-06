from django.utils import timezone
from rest_framework import status

from shop.models import Order

ORDER_LIST = "/api/shop/orders/"


def ORDER_DETAIL(o):
    return f"{ORDER_LIST}{o.order_id}/"


def test_filter_by_status(api_client, orders):
    api_client.force_authenticate(orders["u1"])
    resp = api_client.get(f"{ORDER_LIST}?status=pending")
    assert resp.status_code == 200
    assert {o["status"] for o in resp.data["results"]} == {Order.StatusChoices.PENDING}


def test_filter_total_min(api_client, orders):
    api_client.force_authenticate(orders["u2"])
    resp = api_client.get(f"{ORDER_LIST}?total_min=10")
    assert resp.status_code == 200
    assert len(resp.data["results"]) == 1


def test_filter_total_max(api_client, orders):
    api_client.force_authenticate(orders["u1"])
    resp = api_client.get(f"{ORDER_LIST}?total_max=20")
    assert resp.status_code == 200
    assert len(resp.data["results"]) == 2


def test_filter_created_range(api_client, orders):
    api_client.force_authenticate(orders["u1"])
    past = (timezone.now() - timezone.timedelta(days=365)).date().isoformat()
    resp = api_client.get(f"{ORDER_LIST}?created_after={past}")
    assert resp.status_code == 200


class TestOrderDelete:
    def test_owner_can_delete_pending(self, api_client, orders):
        api_client.force_authenticate(orders["u1"])
        resp = api_client.delete(ORDER_DETAIL(orders["o1"]))
        assert resp.status_code == status.HTTP_204_NO_CONTENT

    def test_owner_cannot_delete_confirmed(self, api_client, orders):
        api_client.force_authenticate(orders["u2"])
        resp = api_client.delete(ORDER_DETAIL(orders["o2"]))
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_delete_any(self, admin_client, orders):
        resp = admin_client.delete(ORDER_DETAIL(orders["o2"]))
        assert resp.status_code == status.HTTP_204_NO_CONTENT

    def test_unauthenticated_delete(self, api_client, orders):
        resp = api_client.delete(ORDER_DETAIL(orders["o1"]))
        assert resp.status_code == status.HTTP_403_FORBIDDEN
