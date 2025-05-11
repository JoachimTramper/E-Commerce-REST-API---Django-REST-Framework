import pytest
from rest_framework import status

CART_LIST = "/api/shop/cart/"
CART_ITEMS_LIST = "/api/shop/cart/items/"


def CART_ITEM_DETAIL(item_id):
    return f"{CART_ITEMS_LIST}{item_id}/"


@pytest.mark.django_db
class TestCartRetrieval:
    def test_get_empty_cart_returns_404(self, auth_client, no_order_user):
        # No pending cart for this user
        auth_client.force_authenticate(no_order_user)
        resp = auth_client.get(CART_LIST)
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_get_cart_with_items(self, auth_client, cart_with_items):
        # Fixture cart_with_items has 2 items in PENDING-cart
        client, cart = auth_client, cart_with_items
        # Authenticated user is the cart owner
        client.force_authenticate(cart.user)
        resp = client.get(CART_LIST)
        assert resp.status_code == status.HTTP_200_OK
        data = resp.data
        assert len(data["items"]) == 2
        totals = sum(float(i["item_subtotal"]) for i in data["items"])
        assert float(data["total_amount"]) == pytest.approx(totals)


@pytest.mark.django_db
class TestCartItemListDirect:
    def test_list_cart_items_directly(self, auth_client, cart_with_items):
        # Fixture cart_with_items has 2 items in PENDING-cart
        client, cart = auth_client, cart_with_items
        client.force_authenticate(cart.user)

        resp = client.get(CART_ITEMS_LIST)
        assert resp.status_code == status.HTTP_200_OK

        data = resp.data
        # Paginate response: count and results
        assert data["count"] == 2
        assert len(data["results"]) == 2

        # Every item belongs to the same order
        returned_orders = {str(it["order"]) for it in data["results"]}
        assert returned_orders == {str(cart.order_id)}


@pytest.mark.django_db
class TestCartItemCRUD:
    def test_create_requires_auth(self, anon_client, products):
        payload = {"product": products[0].pk, "quantity": 1}
        resp = anon_client.post(CART_ITEMS_LIST, payload, format="json")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_add_first_item_creates_cart(self, auth_client, products, no_order_user):
        auth_client.force_authenticate(no_order_user)
        payload = {"product": products[0].pk, "quantity": 2}
        resp = auth_client.post(CART_ITEMS_LIST, payload, format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        data = resp.data
        assert len(data["items"]) == 1
        item = data["items"][0]
        assert item["quantity"] == 2
        assert float(item["item_subtotal"]) == 2 * float(products[0].price)

    def test_add_second_item_appends(self, auth_client, products, no_order_user):
        auth_client.force_authenticate(no_order_user)
        # First item A
        auth_client.post(
            CART_ITEMS_LIST, {"product": products[0].pk, "quantity": 1}, format="json"
        )
        # Second item B
        resp = auth_client.post(
            CART_ITEMS_LIST, {"product": products[2].pk, "quantity": 1}, format="json"
        )
        assert resp.status_code == status.HTTP_201_CREATED
        data = resp.data
        # Now 2 items in cart
        assert len(data["items"]) == 2
        subtotals = {i["item_subtotal"] for i in data["items"]}
        expected = {1 * float(products[0].price), 1 * float(products[2].price)}
        assert subtotals == expected

    def test_patch_item_quantity(self, auth_client, cart_with_items):
        client, cart = auth_client, cart_with_items
        item = cart.items.first()
        client.force_authenticate(cart.user)
        resp = client.patch(
            CART_ITEM_DETAIL(item.id),
            {"quantity": item.quantity + 2},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["quantity"] == item.quantity + 2
        assert float(resp.data["item_subtotal"]) == pytest.approx(
            (item.quantity + 2) * float(item.price)
        )

    def test_delete_single_item_and_cleanup(self, auth_client, cart_with_one_item):
        # Fixture 'cart_with_one_item' has 1 item in PENDING-cart
        client, cart = auth_client, cart_with_one_item
        client.force_authenticate(cart.user)
        item = cart.items.first()
        resp = client.delete(CART_ITEM_DETAIL(item.id))
        # Last item deleted, cart will be deleted too
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        # No more cart
        resp2 = client.get(CART_LIST)
        assert resp2.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_one_of_multiple_items(self, auth_client, cart_with_items):
        client, cart = auth_client, cart_with_items
        client.force_authenticate(cart.user)
        item = cart.items.first()
        resp = client.delete(CART_ITEM_DETAIL(item.id))
        # Cart keeps existing (1 item remains)
        assert resp.status_code == status.HTTP_200_OK
        data = resp.data
        assert len(data["items"]) == 1


@pytest.mark.django_db
class TestCartItemEdgeCases:
    def test_create_invalid_quantities(self, auth_client, products, orders):
        auth_client.force_authenticate(orders["u1"])
        for qty in [0, -5]:
            resp = auth_client.post(
                CART_ITEMS_LIST,
                {"product": products[0].pk, "quantity": qty},
                format="json",
            )
            assert resp.status_code == status.HTTP_400_BAD_REQUEST
            assert "Quantity must be at least 1" in str(resp.data)

    def test_create_exceeds_stock(self, auth_client, products, orders):
        auth_client.force_authenticate(orders["u1"])
        resp = auth_client.post(
            CART_ITEMS_LIST,
            {"product": products[0].pk, "quantity": products[0].stock + 10},
            format="json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "only" in str(resp.data).lower()

    def test_create_on_confirmed_order_starts_new_cart(
        self, auth_client, products, orders
    ):
        auth_client.force_authenticate(orders["u2"])
        payload = {"product": products[0].pk, "quantity": 1}
        resp = auth_client.post(CART_ITEMS_LIST, payload, format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        data = resp.data
        assert len(data["items"]) == 1
        assert data["items"][0]["quantity"] == 1

    def test_patch_nonexistent_returns_404(self, auth_client, orders):
        auth_client.force_authenticate(orders["u1"])
        resp = auth_client.patch(
            CART_ITEM_DETAIL(999999), {"quantity": 1}, format="json"
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_returns_404(self, auth_client, orders):
        auth_client.force_authenticate(orders["u1"])
        resp = auth_client.delete(CART_ITEM_DETAIL(999999))
        assert resp.status_code == status.HTTP_404_NOT_FOUND
