/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Cart } from '../models/Cart';
import type { OrderCreate } from '../models/OrderCreate';
import type { OrderCreateRequest } from '../models/OrderCreateRequest';
import type { OrderDetail } from '../models/OrderDetail';
import type { OrderItemCreateUpdateRequest } from '../models/OrderItemCreateUpdateRequest';
import type { OrderItemDetail } from '../models/OrderItemDetail';
import type { PaginatedOrderCreateList } from '../models/PaginatedOrderCreateList';
import type { PaginatedOrderDetailList } from '../models/PaginatedOrderDetailList';
import type { PaginatedOrderItemDetailList } from '../models/PaginatedOrderItemDetailList';
import type { PaginatedOrderItemListList } from '../models/PaginatedOrderItemListList';
import type { PaginatedProductList } from '../models/PaginatedProductList';
import type { PatchedOrderCreateRequest } from '../models/PatchedOrderCreateRequest';
import type { PatchedOrderItemCreateUpdateRequest } from '../models/PatchedOrderItemCreateUpdateRequest';
import type { PatchedProductRequest } from '../models/PatchedProductRequest';
import type { Product } from '../models/Product';
import type { ProductRequest } from '../models/ProductRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ShopService {
    /**
     * Retrieve the current user's pending cart
     * @returns Cart
     * @throws ApiError
     */
    public static shopCartList(): CancelablePromise<Array<Cart>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/shop/cart/',
            errors: {
                404: `No pending cart`,
            },
        });
    }
    /**
     * Reserve stock and sets status to AWAITING_PAYMENT. Returns 200 + JSON { message: … } if successful.
     * @returns any Stock reserved; you have 10 minutes to complete payment.
     * @throws ApiError
     */
    public static cartCheckout(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/shop/cart/checkout/',
            errors: {
                400: `Not enough stock / concurrency error`,
                404: `No pending cart`,
            },
        });
    }
    /**
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedOrderItemListList
     * @throws ApiError
     */
    public static cartItemsList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedOrderItemListList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/shop/cart/items/',
            query: {
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * @param requestBody
     * @returns Cart
     * @throws ApiError
     */
    public static cartItemCreate(
        requestBody: OrderItemCreateUpdateRequest,
    ): CancelablePromise<Cart> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/shop/cart/items/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param id A unique integer value identifying this order item.
     * @returns OrderItemDetail
     * @throws ApiError
     */
    public static cartItemsRetrieve(
        id: number,
    ): CancelablePromise<OrderItemDetail> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/shop/cart/items/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param id A unique integer value identifying this order item.
     * @param requestBody
     * @returns OrderItemDetail
     * @throws ApiError
     */
    public static cartItemUpdate(
        id: number,
        requestBody: OrderItemCreateUpdateRequest,
    ): CancelablePromise<OrderItemDetail> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/shop/cart/items/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param id A unique integer value identifying this order item.
     * @param requestBody
     * @returns OrderItemDetail
     * @throws ApiError
     */
    public static cartItemPartialUpdate(
        id: number,
        requestBody?: PatchedOrderItemCreateUpdateRequest,
    ): CancelablePromise<OrderItemDetail> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/shop/cart/items/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param id A unique integer value identifying this order item.
     * @returns void
     * @throws ApiError
     */
    public static cartItemDelete(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/shop/cart/items/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * - Admin users: full CRUD on all order items.
     * - Non-staff users:
     * • list/retrieve: only items from their own orders.
     * • create: only if they have at least one PENDING order.
     * • update/partial_update: only on items whose order status == PENDING.
     * • delete: only on items whose order status == PENDING.
     * @param order
     * @param orderStatus * `Pending` - Pending
     * * `AwaitingPayment` - Awaiting Payment
     * * `Confirmed` - Confirmed
     * * `Shipped` - Shipped
     * * `Delivered` - Delivered
     * * `Cancelled` - Cancelled
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param pageSize Number of results to return per page.
     * @param product
     * @param quantityMax
     * @param quantityMin
     * @param search A search term.
     * @returns PaginatedOrderItemDetailList Retrieve order-item
     * @throws ApiError
     */
    public static shopOrderItemsList(
        order?: string,
        orderStatus?: 'AwaitingPayment' | 'Cancelled' | 'Confirmed' | 'Delivered' | 'Pending' | 'Shipped',
        ordering?: string,
        page?: number,
        pageSize?: number,
        product?: number,
        quantityMax?: number,
        quantityMin?: number,
        search?: string,
    ): CancelablePromise<PaginatedOrderItemDetailList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/shop/order-items/',
            query: {
                'order': order,
                'order__status': orderStatus,
                'ordering': ordering,
                'page': page,
                'page_size': pageSize,
                'product': product,
                'quantity_max': quantityMax,
                'quantity_min': quantityMin,
                'search': search,
            },
            errors: {
                400: `Validation error`,
                404: `Not found`,
            },
        });
    }
    /**
     * - Admin users: full CRUD on all order items.
     * - Non-staff users:
     * • list/retrieve: only items from their own orders.
     * • create: only if they have at least one PENDING order.
     * • update/partial_update: only on items whose order status == PENDING.
     * • delete: only on items whose order status == PENDING.
     * @param requestBody
     * @returns OrderItemDetail Retrieve order-item
     * @throws ApiError
     */
    public static shopOrderItemsCreate(
        requestBody: OrderItemCreateUpdateRequest,
    ): CancelablePromise<OrderItemDetail> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/shop/order-items/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Validation error`,
                404: `Not found`,
            },
        });
    }
    /**
     * - Admin users: full CRUD on all order items.
     * - Non-staff users:
     * • list/retrieve: only items from their own orders.
     * • create: only if they have at least one PENDING order.
     * • update/partial_update: only on items whose order status == PENDING.
     * • delete: only on items whose order status == PENDING.
     * @param id A unique integer value identifying this order item.
     * @returns OrderItemDetail Retrieve order-item
     * @throws ApiError
     */
    public static shopOrderItemsRetrieve(
        id: number,
    ): CancelablePromise<OrderItemDetail> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/shop/order-items/{id}/',
            path: {
                'id': id,
            },
            errors: {
                400: `Validation error`,
                404: `Not found`,
            },
        });
    }
    /**
     * - Admin users: full CRUD on all order items.
     * - Non-staff users:
     * • list/retrieve: only items from their own orders.
     * • create: only if they have at least one PENDING order.
     * • update/partial_update: only on items whose order status == PENDING.
     * • delete: only on items whose order status == PENDING.
     * @param id A unique integer value identifying this order item.
     * @param requestBody
     * @returns OrderItemDetail Retrieve order-item
     * @throws ApiError
     */
    public static shopOrderItemsUpdate(
        id: number,
        requestBody: OrderItemCreateUpdateRequest,
    ): CancelablePromise<OrderItemDetail> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/shop/order-items/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Validation error`,
                404: `Not found`,
            },
        });
    }
    /**
     * - Admin users: full CRUD on all order items.
     * - Non-staff users:
     * • list/retrieve: only items from their own orders.
     * • create: only if they have at least one PENDING order.
     * • update/partial_update: only on items whose order status == PENDING.
     * • delete: only on items whose order status == PENDING.
     * @param id A unique integer value identifying this order item.
     * @param requestBody
     * @returns OrderItemDetail Retrieve order-item
     * @throws ApiError
     */
    public static shopOrderItemsPartialUpdate(
        id: number,
        requestBody?: PatchedOrderItemCreateUpdateRequest,
    ): CancelablePromise<OrderItemDetail> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/shop/order-items/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Validation error`,
                404: `Not found`,
            },
        });
    }
    /**
     * - Admin users: full CRUD on all order items.
     * - Non-staff users:
     * • list/retrieve: only items from their own orders.
     * • create: only if they have at least one PENDING order.
     * • update/partial_update: only on items whose order status == PENDING.
     * • delete: only on items whose order status == PENDING.
     * @param id A unique integer value identifying this order item.
     * @returns OrderItemDetail Retrieve order-item
     * @throws ApiError
     */
    public static shopOrderItemsDestroy(
        id: number,
    ): CancelablePromise<OrderItemDetail> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/shop/order-items/{id}/',
            path: {
                'id': id,
            },
            errors: {
                400: `Validation error`,
                404: `Not found`,
            },
        });
    }
    /**
     * - Admin users: full CRUD on all orders.
     * - Non-staff users:
     * • list/retrieve: only their own orders.
     * • create: may create orders for themselves.
     * • update/partial_update: only on their own orders when status == PENDING.
     * • delete: only on their own orders when status == PENDING.
     * @param createdAfter
     * @param createdBefore
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param pageSize Number of results to return per page.
     * @param search A search term.
     * @param status
     * @param totalMax
     * @param totalMin
     * @returns PaginatedOrderDetailList Retrieve order
     * @returns PaginatedOrderCreateList Create order
     * @throws ApiError
     */
    public static shopOrdersList(
        createdAfter?: string,
        createdBefore?: string,
        ordering?: string,
        page?: number,
        pageSize?: number,
        search?: string,
        status?: string,
        totalMax?: number,
        totalMin?: number,
    ): CancelablePromise<PaginatedOrderDetailList | PaginatedOrderCreateList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/shop/orders/',
            query: {
                'created_after': createdAfter,
                'created_before': createdBefore,
                'ordering': ordering,
                'page': page,
                'page_size': pageSize,
                'search': search,
                'status': status,
                'total_max': totalMax,
                'total_min': totalMin,
            },
            errors: {
                400: `Validation error`,
                404: `Not found`,
            },
        });
    }
    /**
     * - Admin users: full CRUD on all orders.
     * - Non-staff users:
     * • list/retrieve: only their own orders.
     * • create: may create orders for themselves.
     * • update/partial_update: only on their own orders when status == PENDING.
     * • delete: only on their own orders when status == PENDING.
     * @param requestBody
     * @returns OrderDetail Retrieve order
     * @returns OrderCreate Create order
     * @throws ApiError
     */
    public static shopOrdersCreate(
        requestBody: OrderCreateRequest,
    ): CancelablePromise<OrderDetail | OrderCreate> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/shop/orders/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Validation error`,
                404: `Not found`,
            },
        });
    }
    /**
     * - Admin users: full CRUD on all orders.
     * - Non-staff users:
     * • list/retrieve: only their own orders.
     * • create: may create orders for themselves.
     * • update/partial_update: only on their own orders when status == PENDING.
     * • delete: only on their own orders when status == PENDING.
     * @param orderId A UUID string identifying this order.
     * @returns OrderDetail Retrieve order
     * @returns OrderCreate Create order
     * @throws ApiError
     */
    public static shopOrdersRetrieve(
        orderId: string,
    ): CancelablePromise<OrderDetail | OrderCreate> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/shop/orders/{order_id}/',
            path: {
                'order_id': orderId,
            },
            errors: {
                400: `Validation error`,
                404: `Not found`,
            },
        });
    }
    /**
     * - Admin users: full CRUD on all orders.
     * - Non-staff users:
     * • list/retrieve: only their own orders.
     * • create: may create orders for themselves.
     * • update/partial_update: only on their own orders when status == PENDING.
     * • delete: only on their own orders when status == PENDING.
     * @param orderId A UUID string identifying this order.
     * @param requestBody
     * @returns OrderDetail Retrieve order
     * @returns OrderCreate Create order
     * @throws ApiError
     */
    public static shopOrdersUpdate(
        orderId: string,
        requestBody: OrderCreateRequest,
    ): CancelablePromise<OrderDetail | OrderCreate> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/shop/orders/{order_id}/',
            path: {
                'order_id': orderId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Validation error`,
                404: `Not found`,
            },
        });
    }
    /**
     * - Admin users: full CRUD on all orders.
     * - Non-staff users:
     * • list/retrieve: only their own orders.
     * • create: may create orders for themselves.
     * • update/partial_update: only on their own orders when status == PENDING.
     * • delete: only on their own orders when status == PENDING.
     * @param orderId A UUID string identifying this order.
     * @param requestBody
     * @returns OrderDetail Retrieve order
     * @returns OrderCreate Create order
     * @throws ApiError
     */
    public static shopOrdersPartialUpdate(
        orderId: string,
        requestBody?: PatchedOrderCreateRequest,
    ): CancelablePromise<OrderDetail | OrderCreate> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/shop/orders/{order_id}/',
            path: {
                'order_id': orderId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Validation error`,
                404: `Not found`,
            },
        });
    }
    /**
     * - Admin users: full CRUD on all orders.
     * - Non-staff users:
     * • list/retrieve: only their own orders.
     * • create: may create orders for themselves.
     * • update/partial_update: only on their own orders when status == PENDING.
     * • delete: only on their own orders when status == PENDING.
     * @param orderId A UUID string identifying this order.
     * @returns OrderDetail Retrieve order
     * @returns OrderCreate Create order
     * @throws ApiError
     */
    public static shopOrdersDestroy(
        orderId: string,
    ): CancelablePromise<OrderDetail | OrderCreate> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/shop/orders/{order_id}/',
            path: {
                'order_id': orderId,
            },
            errors: {
                400: `Validation error`,
                404: `Not found`,
            },
        });
    }
    /**
     * @param inStock
     * @param name
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param pageSize Number of results to return per page.
     * @param priceMax
     * @param priceMin
     * @param search A search term.
     * @returns PaginatedProductList Retrieve product
     * @throws ApiError
     */
    public static shopProductsList(
        inStock?: boolean,
        name?: string,
        ordering?: string,
        page?: number,
        pageSize?: number,
        priceMax?: number,
        priceMin?: number,
        search?: string,
    ): CancelablePromise<PaginatedProductList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/shop/products/',
            query: {
                'in_stock': inStock,
                'name': name,
                'ordering': ordering,
                'page': page,
                'page_size': pageSize,
                'price_max': priceMax,
                'price_min': priceMin,
                'search': search,
            },
            errors: {
                400: `Validation error`,
                404: `Not found`,
            },
        });
    }
    /**
     * @param requestBody
     * @returns Product Retrieve product
     * @throws ApiError
     */
    public static shopProductsCreate(
        requestBody: ProductRequest,
    ): CancelablePromise<Product> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/shop/products/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Validation error`,
                404: `Not found`,
            },
        });
    }
    /**
     * @param id A unique integer value identifying this product.
     * @returns Product Retrieve product
     * @throws ApiError
     */
    public static shopProductsRetrieve(
        id: number,
    ): CancelablePromise<Product> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/shop/products/{id}/',
            path: {
                'id': id,
            },
            errors: {
                400: `Validation error`,
                404: `Not found`,
            },
        });
    }
    /**
     * @param id A unique integer value identifying this product.
     * @param requestBody
     * @returns Product Retrieve product
     * @throws ApiError
     */
    public static shopProductsUpdate(
        id: number,
        requestBody: ProductRequest,
    ): CancelablePromise<Product> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/shop/products/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Validation error`,
                404: `Not found`,
            },
        });
    }
    /**
     * @param id A unique integer value identifying this product.
     * @param requestBody
     * @returns Product Retrieve product
     * @throws ApiError
     */
    public static shopProductsPartialUpdate(
        id: number,
        requestBody?: PatchedProductRequest,
    ): CancelablePromise<Product> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/shop/products/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Validation error`,
                404: `Not found`,
            },
        });
    }
    /**
     * @param id A unique integer value identifying this product.
     * @returns Product Retrieve product
     * @throws ApiError
     */
    public static shopProductsDestroy(
        id: number,
    ): CancelablePromise<Product> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/shop/products/{id}/',
            path: {
                'id': id,
            },
            errors: {
                400: `Validation error`,
                404: `Not found`,
            },
        });
    }
}
