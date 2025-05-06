import pytest
from rest_framework import status

ITEM_LIST = "/api/shop/order-items/"


def ITEM_DETAIL(i):
    return f"{ITEM_LIST}{i.id}/"


def test_filter_by_order(item_client, items):
    resp = item_client.get(f"{ITEM_LIST}?order={items['i1'].order.order_id}")
    assert resp.status_code == 200
    assert all(
        i["order"] == str(items["i1"].order.order_id) for i in resp.data["results"]
    )


def test_filter_by_product_on_order_items(item_client, items):
    product_id = items["p1"].id
    resp = item_client.get(f"{ITEM_LIST}?product={product_id}")
    assert resp.status_code == 200
    quantities = {it["quantity"] for it in resp.data["results"]}
    # 2 items, quantities 1 and 2
    assert quantities == {1, 2}


@pytest.mark.parametrize(
    "param,val,expected_qties",
    [
        ("quantity_min", 2, {2, 3}),
        ("quantity_max", 2, {1, 2}),
    ],
)
def test_item_quantity_filters(item_client, items, param, val, expected_qties):
    resp = item_client.get(f"{ITEM_LIST}?{param}={val}")
    assert resp.status_code == 200
    qtys = {i["quantity"] for i in resp.data["results"]}
    assert qtys == expected_qties


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
