import pytest
from django.utils import timezone
from rest_framework import status

from shop.models import Order

ORDER_LIST = "/api/shop/orders/"
CART_LIST = "/api/shop/cart/"


def ORDER_DETAIL(o):
    order_id = o.order_id if hasattr(o, "order_id") else o
    return f"{ORDER_LIST}{order_id}/"


@pytest.mark.django_db
class TestOrderFiltering:
    def test_filter_by_status(self, api_client, orders):
        api_client.force_authenticate(orders["u1"])
        resp = api_client.get(f"{ORDER_LIST}?status=pending")
        assert resp.status_code == 200
        assert {o["status"] for o in resp.data["results"]} == {
            Order.StatusChoices.PENDING
        }

    def test_filter_total_min(self, api_client, orders):
        api_client.force_authenticate(orders["u2"])
        resp = api_client.get(f"{ORDER_LIST}?total_min=10")
        assert resp.status_code == 200
        assert len(resp.data["results"]) == 1

    def test_filter_total_max(self, api_client, orders):
        api_client.force_authenticate(orders["u1"])
        resp = api_client.get(f"{ORDER_LIST}?total_max=20")
        assert resp.status_code == 200
        assert len(resp.data["results"]) == 2

    def test_filter_created_range(self, api_client, orders):
        api_client.force_authenticate(orders["u1"])
        past = (timezone.now() - timezone.timedelta(days=365)).date().isoformat()
        resp = api_client.get(f"{ORDER_LIST}?created_after={past}")
        assert resp.status_code == 200


@pytest.mark.django_db
class TestOrderCRUD:
    def test_list_only_my_orders(self, api_client, orders):
        api_client.force_authenticate(orders["u1"])
        resp = api_client.get(ORDER_LIST)
        assert resp.status_code == status.HTTP_200_OK
        # check no other orders are returned
        order_ids = {o["order_id"] for o in resp.data["results"]}
        assert order_ids == {str(orders["o1"].order_id), str(orders["o3"].order_id)}

    def test_retrieve_my_order(self, api_client, orders):
        api_client.force_authenticate(orders["u1"])
        resp = api_client.get(ORDER_DETAIL(orders["o1"]))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["order_number"] == orders["o1"].order_number

    def test_retrieve_other_order_404(self, auth_client, orders):
        auth_client.force_authenticate(orders["u1"])
        resp = auth_client.get(ORDER_DETAIL(orders["o2"]))
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_admin_can_retrieve_any(self, admin_client, orders):
        resp = admin_client.get(ORDER_DETAIL(orders["o2"]))
        assert resp.status_code == status.HTTP_200_OK

    def test_update_my_pending_order(self, api_client, orders):
        api_client.force_authenticate(orders["u1"])
        url = ORDER_DETAIL(orders["o1"])
        resp = api_client.patch(
            url,
            {"status": Order.StatusChoices.CONFIRMED},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["status"] == Order.StatusChoices.CONFIRMED

    def test_update_non_pending_forbidden(self, auth_client, orders):
        url = ORDER_DETAIL(orders["o2"])
        resp = auth_client.patch(
            url,
            {"status": Order.StatusChoices.CANCELLED},
            format="json",
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_nonexistent_returns_404(self, admin_client):
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        resp = admin_client.patch(
            ORDER_DETAIL(fake_uuid),
            {"status": Order.StatusChoices.SHIPPED},
            format="json",
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestOrderPermissions:
    def test_non_admin_cannot_create_order(self, auth_client, user):
        auth_client.force_authenticate(user=user)
        payload = {"items": []}
        resp = auth_client.post(ORDER_LIST, payload, format="json")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_create_order(self, admin_client, products):
        payload = {"items": [{"product_id": products[0].pk, "quantity": 1}]}
        resp = admin_client.post(ORDER_LIST, payload, format="json")
        assert resp.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
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
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestOrderEdgeCases:
    def test_admin_can_update_any_order(self, admin_client, orders):
        for o in (orders["o1"], orders["o2"], orders["o3"]):
            resp = admin_client.patch(
                ORDER_DETAIL(o), {"status": Order.StatusChoices.SHIPPED}, format="json"
            )
            assert resp.status_code == status.HTTP_200_OK
            assert resp.data["status"] == Order.StatusChoices.SHIPPED

    def test_order_ordering_and_search(self, auth_client, orders):
        auth_client.force_authenticate(orders["u1"])
        resp = auth_client.get(f"{ORDER_LIST}?ordering=-total_amount")
        totals = [float(o["total_amount"]) for o in resp.data["results"]]
        assert totals == sorted(totals, reverse=True)

        resp = auth_client.get(f"{ORDER_LIST}?search=pending")
        statuses = {o["status"] for o in resp.data["results"]}
        assert statuses == {Order.StatusChoices.PENDING}

    def test_pagination_parameters(self, auth_client, orders):
        auth_client.force_authenticate(orders["u1"])
        resp = auth_client.get(f"{ORDER_LIST}?page_size=1&page=2")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] > 1
        assert len(resp.data["results"]) == 1
