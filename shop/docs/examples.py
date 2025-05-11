from drf_spectacular.utils import OpenApiExample

PRODUCT_EXAMPLES = [
    OpenApiExample(
        name="Create T-shirt",
        summary="Payload to create a new T-shirt",
        value={
            "name": "T-shirt",
            "price": "19.99",
            "stock": 100,
            "description": "Soft cotton T-shirt",
        },
        request_only=True,
    ),
    OpenApiExample(
        name="Get product response",
        summary="Example response body",
        value={
            "id": 1,
            "name": "T-shirt",
            "price": "19.99",
            "stock": 100,
            "description": "Soft cotton T-shirt",
            "created_at": "2025-05-01T12:34:56Z",
        },
        response_only=True,
    ),
]

ORDER_EXAMPLES = [
    OpenApiExample(
        name="Create order",
        summary="Payload to create a new order",
        value={
            "items": [
                {"product_id": 1, "quantity": 2, "price": "19.99"},
                {"product_id": 2, "quantity": 1, "price": "5.00"},
            ]
        },
        request_only=True,
    ),
    OpenApiExample(
        name="Get order response",
        summary="Example response for retrieving an order",
        value={
            "order_id": "123e4567-e89b-12d3-a456-426655440000",
            "status": "pending",
            "total_amount": "44.98",
            "created_at": "2025-05-10T14:00:00Z",
            "items": [
                {
                    "id": 1,
                    "product_id": 1,
                    "product_name": "T-shirt",
                    "quantity": 2,
                    "price": "19.99",
                    "item_subtotal": "39.98",
                },
                {
                    "id": 2,
                    "product_id": 2,
                    "product_name": "Socks",
                    "quantity": 1,
                    "price": "5.00",
                    "item_subtotal": "5.00",
                },
            ],
        },
        response_only=True,
    ),
]

ORDER_ITEM_EXAMPLES = [
    OpenApiExample(
        name="Create order item",
        summary="Payload to add an item to an existing order",
        value={"product": 2, "quantity": 3},
        request_only=True,
    ),
    OpenApiExample(
        name="Get order-item response",
        summary="Example response for order-item",
        value={
            "id": 5,
            "order": "123e4567-e89b-12d3-a456-426655440000",
            "product": 2,
            "product_name": "Socks",
            "quantity": 3,
            "item_subtotal": "15.00",
        },
        response_only=True,
    ),
]

CART_EXAMPLES = [
    OpenApiExample(
        name="Get cart empty",
        summary="Lege cart response",
        value={"items": [], "total_amount": "0.00"},
        response_only=True,
    ),
    OpenApiExample(
        name="Get cart with items",
        summary="Response van een cart met 2 items",
        value={
            "order_id": "123e4567-e89b-12d3-a456-426614174000",
            "order_number": 7,
            "created_at": "2025-05-11T12:34:56.789Z",
            "status": "pending",
            "items": [
                {
                    "id": 1,
                    "order": "123e4567-e89b-12d3-a456-426614174000",
                    "product": 1,
                    "quantity": 2,
                    "item_subtotal": "20.00",
                },
                {
                    "id": 2,
                    "order": "123e4567-e89b-12d3-a456-426614174000",
                    "product": 2,
                    "quantity": 1,
                    "item_subtotal": "5.00",
                },
            ],
            "total_amount": "25.00",
        },
        response_only=True,
    ),
]

CART_ITEM_EXAMPLES = [
    OpenApiExample(
        name="Add item to cart",
        summary="Voeg 2 stuks van product #1 toe",
        value={"product": 1, "quantity": 2},
        request_only=True,
    ),
]
