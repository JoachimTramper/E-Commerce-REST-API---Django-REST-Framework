import pytest
from django.utils import timezone
from rest_framework import status

from shop.models import Order

ORDER_LIST = "/api/shop/orders/"


def ORDER_DETAIL(o):
    order_id = o.order_id if hasattr(o, "order_id") else o
    return f"{ORDER_LIST}{order_id}/"


@pytest.mark.django_db
class TestOrderFiltering:
    def test_filter_by_status(self, anon_client, orders):
        anon_client.force_authenticate(orders["u1"])
        resp = anon_client.get(f"{ORDER_LIST}?status=pending")
        assert resp.status_code == 200
        assert {o["status"] for o in resp.data["results"]} == {
            Order.StatusChoices.PENDING
        }

    def test_filter_total_min(self, anon_client, orders):
        anon_client.force_authenticate(orders["u2"])
        resp = anon_client.get(f"{ORDER_LIST}?total_min=10")
        assert resp.status_code == 200
        assert len(resp.data["results"]) == 1

    def test_filter_total_max(self, anon_client, orders):
        anon_client.force_authenticate(orders["u1"])
        resp = anon_client.get(f"{ORDER_LIST}?total_max=20")
        assert resp.status_code == 200
        assert len(resp.data["results"]) == 2

    def test_filter_created_range(self, anon_client, orders):
        anon_client.force_authenticate(orders["u1"])
        past = (timezone.now() - timezone.timedelta(days=365)).date().isoformat()
        resp = anon_client.get(f"{ORDER_LIST}?created_after={past}")
        assert resp.status_code == 200


@pytest.mark.django_db
class TestOrderCRUD:
    def test_list_only_my_orders(self, anon_client, orders):
        anon_client.force_authenticate(orders["u1"])
        resp = anon_client.get(ORDER_LIST)
        assert resp.status_code == status.HTTP_200_OK
        # check no other orders are returned
        order_ids = {o["order_id"] for o in resp.data["results"]}
        assert order_ids == {str(orders["o1"].order_id), str(orders["o3"].order_id)}

    def test_retrieve_my_order(self, anon_client, orders):
        anon_client.force_authenticate(orders["u1"])
        resp = anon_client.get(ORDER_DETAIL(orders["o1"]))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["order_number"] == orders["o1"].order_number

    def test_retrieve_other_order_404(self, auth_client, orders):
        auth_client.force_authenticate(orders["u1"])
        resp = auth_client.get(ORDER_DETAIL(orders["o2"]))
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_admin_can_retrieve_any(self, admin_client, orders):
        resp = admin_client.get(ORDER_DETAIL(orders["o2"]))
        assert resp.status_code == status.HTTP_200_OK

    def test_create_requires_auth(self, anon_client, products):
        payload = {"items": [{"product": products[0].pk, "quantity": 1}]}
        resp = anon_client.post(ORDER_LIST, payload, format="json")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_order_success(self, auth_client, products, orders):
        auth_client.force_authenticate(orders["u1"])
        payload = {
            "items": [
                {
                    "product_id": products[0].pk,
                    "quantity": 2,
                    "price": str(products[0].price),
                },
                {
                    "product_id": products[2].pk,
                    "quantity": 1,
                    "price": str(products[2].price),
                },
            ]
        }
        resp = auth_client.post(ORDER_LIST, payload, format="json")
        assert resp.status_code == status.HTTP_201_CREATED, resp.data
        subtotals = [float(i["item_subtotal"]) for i in resp.data["items"]]
        expected = [
            2 * float(products[0].price),
            1 * float(products[2].price),
        ]
        assert subtotals == expected

    def test_update_my_pending_order(self, anon_client, orders):
        anon_client.force_authenticate(orders["u1"])
        url = ORDER_DETAIL(orders["o1"])
        resp = anon_client.patch(
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


class TestOrderDelete:
    def test_owner_can_delete_pending(self, anon_client, orders):
        anon_client.force_authenticate(orders["u1"])
        resp = anon_client.delete(ORDER_DETAIL(orders["o1"]))
        assert resp.status_code == status.HTTP_204_NO_CONTENT

    def test_owner_cannot_delete_confirmed(self, anon_client, orders):
        anon_client.force_authenticate(orders["u2"])
        resp = anon_client.delete(ORDER_DETAIL(orders["o2"]))
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_delete_any(self, admin_client, orders):
        resp = admin_client.delete(ORDER_DETAIL(orders["o2"]))
        assert resp.status_code == status.HTTP_204_NO_CONTENT

    def test_unauthenticated_delete(self, anon_client, orders):
        resp = anon_client.delete(ORDER_DETAIL(orders["o1"]))
        assert resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestOrderEdgeCases:
    def test_create_invalid_payload_returns_400(self, auth_client, products):
        resp = auth_client.post(ORDER_LIST, {}, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        payload = {
            "items": [
                {
                    "product_id": products[0].pk,
                    "quantity": 9999,
                    "price": str(products[0].price),
                }
            ]
        }
        resp = auth_client.post(ORDER_LIST, payload, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "You ordered" in resp.data["items"][0]["quantity"][0]

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
