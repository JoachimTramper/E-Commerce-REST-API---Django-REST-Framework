import pytest
from rest_framework import status

ITEM_LIST = "/api/shop/order-items/"


def ITEM_DETAIL(i):
    return f"{ITEM_LIST}{i.id}/"


@pytest.mark.django_db
class TestOrderItemFiltering:
    def test_filter_by_order(self, item_client, items):
        resp = item_client.get(f"{ITEM_LIST}?order={items['i1'].order.order_id}")
        assert resp.status_code == 200
        assert all(
            i["order"] == str(items["i1"].order.order_id) for i in resp.data["results"]
        )

    def test_filter_by_product_on_order_items(self, item_client, items):
        product_id = items["p1"].id
        resp = item_client.get(f"{ITEM_LIST}?product={product_id}")
        assert resp.status_code == 200
        quantities = {it["quantity"] for it in resp.data["results"]}
        assert quantities == {1, 2}

    @pytest.mark.parametrize(
        "param,val,expected",
        [
            ("quantity_min", 2, {2, 3}),
            ("quantity_max", 2, {1, 2}),
        ],
    )
    def test_item_quantity_filters(self, item_client, items, param, val, expected):
        resp = item_client.get(f"{ITEM_LIST}?{param}={val}")
        assert resp.status_code == 200
        qtys = {i["quantity"] for i in resp.data["results"]}
        assert qtys == expected


@pytest.mark.django_db
class TestOrderItemCRUD:
    def test_list_only_my_items(self, item_client, items):
        resp = item_client.get(ITEM_LIST)
        assert resp.status_code == status.HTTP_200_OK
        ids = {i["id"] for i in resp.data["results"]}
        assert ids == {items["i1"].id, items["i2"].id}

    def test_retrieve_my_item(self, item_client, items):
        resp = item_client.get(ITEM_DETAIL(items["i1"]))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["quantity"] == items["i1"].quantity

    def test_retrieve_other_item_404(self, item_client, items):
        resp = item_client.get(ITEM_DETAIL(items["i3"]))
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_admin_can_retrieve_any(self, admin_client, items):
        resp = admin_client.get(ITEM_DETAIL(items["i3"]))
        assert resp.status_code == status.HTTP_200_OK

    def test_create_requires_auth(self, anon_client, products, orders):
        payload = {"product": products[0].pk, "quantity": 1}
        resp = anon_client.post(ITEM_LIST, payload, format="json")
        print("STATUS:", resp.status_code)
        print("DATA:  ", resp.data)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_success(self, item_client, items):
        # Create on the pending order belonging to items['user']
        payload = {"product": items["p2"].id, "quantity": 2}
        resp = item_client.post(ITEM_LIST, payload, format="json")
        assert resp.status_code == status.HTTP_201_CREATED, resp.data
        data = resp.data
        assert data["product"] == items["p2"].id
        assert data["quantity"] == 2
        assert float(data["item_subtotal"]) == 2 * float(items["p2"].price)

    def test_patch_nonexistent_returns_404(self, admin_client):
        fake_id = 999999
        resp = admin_client.patch(
            f"{ITEM_LIST}{fake_id}/", {"quantity": 1}, format="json"
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestOrderItemDelete:
    def test_owner_can_delete_on_pending(self, item_client, items):
        resp = item_client.delete(ITEM_DETAIL(items["i1"]))
        assert resp.status_code == status.HTTP_204_NO_CONTENT

    def test_owner_cannot_delete_on_confirmed(self, item_client, items):
        resp = item_client.delete(ITEM_DETAIL(items["i3"]))
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_delete_any(self, admin_client, items):
        resp = admin_client.delete(ITEM_DETAIL(items["i3"]))
        assert resp.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestOrderItemEdgeCases:
    def test_create_invalid_quantities(self, item_client, products, orders):
        # zero or negative
        for qty in [0, -1]:
            payload = {"product": products[0].id, "quantity": qty}
            resp = item_client.post(ITEM_LIST, payload, format="json")
            assert resp.status_code == status.HTTP_400_BAD_REQUEST
            assert "Quantity must be at least 1" in str(resp.data)

        # exceeding stock
        payload = {"product": products[0].id, "quantity": 9999}
        resp = item_client.post(ITEM_LIST, payload, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "only" in str(resp.data).lower()

    def test_create_on_confirmed_order_forbidden(self, anon_client, orders, products):
        anon_client.force_authenticate(user=orders["u2"])
        payload = {"product": products[2].id, "quantity": 1}
        resp = anon_client.post(ITEM_LIST, payload, format="json")
        assert resp.status_code in (
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        )

    def test_update_owner_pending(self, item_client, items):
        item = items["i1"]
        resp = item_client.patch(
            ITEM_DETAIL(item), {"quantity": item.quantity + 1}, format="json"
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["quantity"] == item.quantity + 1

    def test_update_owner_confirmed_forbidden(self, item_client, items):
        item = items["i3"]
        resp = item_client.patch(ITEM_DETAIL(item), {"quantity": 5}, format="json")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_update_any(self, admin_client, items):
        item = items["i3"]
        resp = admin_client.patch(ITEM_DETAIL(item), {"quantity": 10}, format="json")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["quantity"] == 10

    def test_ordering_search_pagination(self, item_client, items):
        # ordering by quantity desc
        resp = item_client.get(f"{ITEM_LIST}?ordering=-quantity")
        assert resp.status_code == status.HTTP_200_OK
        qties = [i["quantity"] for i in resp.data["results"]]
        assert qties == sorted(qties, reverse=True)

        # search by product name substring
        substr = items["i1"].product.name[:3]
        resp = item_client.get(f"{ITEM_LIST}?search={substr}")
        assert resp.status_code == status.HTTP_200_OK
        assert all(
            substr.lower() in it["product_name"].lower() for it in resp.data["results"]
        )

        # pagination
        resp = item_client.get(f"{ITEM_LIST}?page_size=1&page=2")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] > 1
        assert len(resp.data["results"]) == 1
