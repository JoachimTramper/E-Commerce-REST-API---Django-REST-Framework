# ShopApi

All URIs are relative to */api*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**cartCheckout**](#cartcheckout) | **POST** /shop/cart/checkout/ | |
|[**cartItemCreate**](#cartitemcreate) | **POST** /shop/cart/items/ | |
|[**cartItemDelete**](#cartitemdelete) | **DELETE** /shop/cart/items/{id}/ | |
|[**cartItemPartialUpdate**](#cartitempartialupdate) | **PATCH** /shop/cart/items/{id}/ | |
|[**cartItemUpdate**](#cartitemupdate) | **PUT** /shop/cart/items/{id}/ | |
|[**cartItemsList**](#cartitemslist) | **GET** /shop/cart/items/ | |
|[**cartItemsRetrieve**](#cartitemsretrieve) | **GET** /shop/cart/items/{id}/ | |
|[**shopCartList**](#shopcartlist) | **GET** /shop/cart/ | |
|[**shopOrderItemsCreate**](#shoporderitemscreate) | **POST** /shop/order-items/ | |
|[**shopOrderItemsDestroy**](#shoporderitemsdestroy) | **DELETE** /shop/order-items/{id}/ | |
|[**shopOrderItemsList**](#shoporderitemslist) | **GET** /shop/order-items/ | |
|[**shopOrderItemsPartialUpdate**](#shoporderitemspartialupdate) | **PATCH** /shop/order-items/{id}/ | |
|[**shopOrderItemsRetrieve**](#shoporderitemsretrieve) | **GET** /shop/order-items/{id}/ | |
|[**shopOrderItemsUpdate**](#shoporderitemsupdate) | **PUT** /shop/order-items/{id}/ | |
|[**shopOrdersCreate**](#shoporderscreate) | **POST** /shop/orders/ | |
|[**shopOrdersDestroy**](#shopordersdestroy) | **DELETE** /shop/orders/{order_id}/ | |
|[**shopOrdersList**](#shoporderslist) | **GET** /shop/orders/ | |
|[**shopOrdersPartialUpdate**](#shoporderspartialupdate) | **PATCH** /shop/orders/{order_id}/ | |
|[**shopOrdersRetrieve**](#shopordersretrieve) | **GET** /shop/orders/{order_id}/ | |
|[**shopOrdersUpdate**](#shopordersupdate) | **PUT** /shop/orders/{order_id}/ | |
|[**shopProductsCreate**](#shopproductscreate) | **POST** /shop/products/ | |
|[**shopProductsDestroy**](#shopproductsdestroy) | **DELETE** /shop/products/{id}/ | |
|[**shopProductsList**](#shopproductslist) | **GET** /shop/products/ | |
|[**shopProductsPartialUpdate**](#shopproductspartialupdate) | **PATCH** /shop/products/{id}/ | |
|[**shopProductsRetrieve**](#shopproductsretrieve) | **GET** /shop/products/{id}/ | |
|[**shopProductsUpdate**](#shopproductsupdate) | **PUT** /shop/products/{id}/ | |

# **cartCheckout**
> cartCheckout()

Reserve stock and sets status to AWAITING_PAYMENT. Returns 200 + JSON { message: … } if successful.

### Example

```typescript
import {
    ShopApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

const { status, data } = await apiInstance.cartCheckout();
```

### Parameters
This endpoint does not have any parameters.


### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Stock reserved; you have 10 minutes to complete payment. |  -  |
|**400** | Not enough stock / concurrency error |  -  |
|**404** | No pending cart |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **cartItemCreate**
> Cart cartItemCreate(orderItemCreateUpdateRequest)


### Example

```typescript
import {
    ShopApi,
    Configuration,
    OrderItemCreateUpdateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let orderItemCreateUpdateRequest: OrderItemCreateUpdateRequest; //

const { status, data } = await apiInstance.cartItemCreate(
    orderItemCreateUpdateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **orderItemCreateUpdateRequest** | **OrderItemCreateUpdateRequest**|  | |


### Return type

**Cart**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **cartItemDelete**
> cartItemDelete()


### Example

```typescript
import {
    ShopApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let id: number; //A unique integer value identifying this order item. (default to undefined)

const { status, data } = await apiInstance.cartItemDelete(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this order item. | defaults to undefined|


### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**204** | Cart item deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **cartItemPartialUpdate**
> OrderItemDetail cartItemPartialUpdate()


### Example

```typescript
import {
    ShopApi,
    Configuration,
    PatchedOrderItemCreateUpdateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let id: number; //A unique integer value identifying this order item. (default to undefined)
let patchedOrderItemCreateUpdateRequest: PatchedOrderItemCreateUpdateRequest; // (optional)

const { status, data } = await apiInstance.cartItemPartialUpdate(
    id,
    patchedOrderItemCreateUpdateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedOrderItemCreateUpdateRequest** | **PatchedOrderItemCreateUpdateRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this order item. | defaults to undefined|


### Return type

**OrderItemDetail**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **cartItemUpdate**
> OrderItemDetail cartItemUpdate(orderItemCreateUpdateRequest)


### Example

```typescript
import {
    ShopApi,
    Configuration,
    OrderItemCreateUpdateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let id: number; //A unique integer value identifying this order item. (default to undefined)
let orderItemCreateUpdateRequest: OrderItemCreateUpdateRequest; //

const { status, data } = await apiInstance.cartItemUpdate(
    id,
    orderItemCreateUpdateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **orderItemCreateUpdateRequest** | **OrderItemCreateUpdateRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this order item. | defaults to undefined|


### Return type

**OrderItemDetail**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **cartItemsList**
> PaginatedOrderItemListList cartItemsList()


### Example

```typescript
import {
    ShopApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)

const { status, data } = await apiInstance.cartItemsList(
    ordering,
    page,
    search
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|


### Return type

**PaginatedOrderItemListList**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **cartItemsRetrieve**
> OrderItemDetail cartItemsRetrieve()


### Example

```typescript
import {
    ShopApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let id: number; //A unique integer value identifying this order item. (default to undefined)

const { status, data } = await apiInstance.cartItemsRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this order item. | defaults to undefined|


### Return type

**OrderItemDetail**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopCartList**
> Array<Cart> shopCartList()

Retrieve the current user\'s pending cart

### Example

```typescript
import {
    ShopApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

const { status, data } = await apiInstance.shopCartList();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**Array<Cart>**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**404** | No pending cart |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopOrderItemsCreate**
> OrderItemDetail shopOrderItemsCreate(orderItemCreateUpdateRequest)

- Admin users: full CRUD on all order items. - Non-staff users:     • list/retrieve: only items from their own orders.     • create: only if they have at least one PENDING order.     • update/partial_update: only on items whose order status == PENDING.     • delete: only on items whose order status == PENDING.

### Example

```typescript
import {
    ShopApi,
    Configuration,
    OrderItemCreateUpdateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let orderItemCreateUpdateRequest: OrderItemCreateUpdateRequest; //

const { status, data } = await apiInstance.shopOrderItemsCreate(
    orderItemCreateUpdateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **orderItemCreateUpdateRequest** | **OrderItemCreateUpdateRequest**|  | |


### Return type

**OrderItemDetail**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Retrieve order-item |  -  |
|**201** | Create order-item |  -  |
|**400** | Validation error |  -  |
|**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopOrderItemsDestroy**
> OrderItemDetail shopOrderItemsDestroy()

- Admin users: full CRUD on all order items. - Non-staff users:     • list/retrieve: only items from their own orders.     • create: only if they have at least one PENDING order.     • update/partial_update: only on items whose order status == PENDING.     • delete: only on items whose order status == PENDING.

### Example

```typescript
import {
    ShopApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let id: number; //A unique integer value identifying this order item. (default to undefined)

const { status, data } = await apiInstance.shopOrderItemsDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this order item. | defaults to undefined|


### Return type

**OrderItemDetail**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Retrieve order-item |  -  |
|**201** | Create order-item |  -  |
|**400** | Validation error |  -  |
|**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopOrderItemsList**
> PaginatedOrderItemDetailList shopOrderItemsList()

- Admin users: full CRUD on all order items. - Non-staff users:     • list/retrieve: only items from their own orders.     • create: only if they have at least one PENDING order.     • update/partial_update: only on items whose order status == PENDING.     • delete: only on items whose order status == PENDING.

### Example

```typescript
import {
    ShopApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let order: string; // (optional) (default to undefined)
let orderStatus: 'AwaitingPayment' | 'Cancelled' | 'Confirmed' | 'Delivered' | 'Pending' | 'Shipped'; //* `Pending` - Pending * `AwaitingPayment` - Awaiting Payment * `Confirmed` - Confirmed * `Shipped` - Shipped * `Delivered` - Delivered * `Cancelled` - Cancelled (optional) (default to undefined)
let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let pageSize: number; //Number of results to return per page. (optional) (default to undefined)
let product: number; // (optional) (default to undefined)
let quantityMax: number; // (optional) (default to undefined)
let quantityMin: number; // (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)

const { status, data } = await apiInstance.shopOrderItemsList(
    order,
    orderStatus,
    ordering,
    page,
    pageSize,
    product,
    quantityMax,
    quantityMin,
    search
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **order** | [**string**] |  | (optional) defaults to undefined|
| **orderStatus** | [**&#39;AwaitingPayment&#39; | &#39;Cancelled&#39; | &#39;Confirmed&#39; | &#39;Delivered&#39; | &#39;Pending&#39; | &#39;Shipped&#39;**]**Array<&#39;AwaitingPayment&#39; &#124; &#39;Cancelled&#39; &#124; &#39;Confirmed&#39; &#124; &#39;Delivered&#39; &#124; &#39;Pending&#39; &#124; &#39;Shipped&#39;>** | * &#x60;Pending&#x60; - Pending * &#x60;AwaitingPayment&#x60; - Awaiting Payment * &#x60;Confirmed&#x60; - Confirmed * &#x60;Shipped&#x60; - Shipped * &#x60;Delivered&#x60; - Delivered * &#x60;Cancelled&#x60; - Cancelled | (optional) defaults to undefined|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **pageSize** | [**number**] | Number of results to return per page. | (optional) defaults to undefined|
| **product** | [**number**] |  | (optional) defaults to undefined|
| **quantityMax** | [**number**] |  | (optional) defaults to undefined|
| **quantityMin** | [**number**] |  | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|


### Return type

**PaginatedOrderItemDetailList**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Retrieve order-item |  -  |
|**201** | Create order-item |  -  |
|**400** | Validation error |  -  |
|**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopOrderItemsPartialUpdate**
> OrderItemDetail shopOrderItemsPartialUpdate()

- Admin users: full CRUD on all order items. - Non-staff users:     • list/retrieve: only items from their own orders.     • create: only if they have at least one PENDING order.     • update/partial_update: only on items whose order status == PENDING.     • delete: only on items whose order status == PENDING.

### Example

```typescript
import {
    ShopApi,
    Configuration,
    PatchedOrderItemCreateUpdateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let id: number; //A unique integer value identifying this order item. (default to undefined)
let patchedOrderItemCreateUpdateRequest: PatchedOrderItemCreateUpdateRequest; // (optional)

const { status, data } = await apiInstance.shopOrderItemsPartialUpdate(
    id,
    patchedOrderItemCreateUpdateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedOrderItemCreateUpdateRequest** | **PatchedOrderItemCreateUpdateRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this order item. | defaults to undefined|


### Return type

**OrderItemDetail**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Retrieve order-item |  -  |
|**201** | Create order-item |  -  |
|**400** | Validation error |  -  |
|**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopOrderItemsRetrieve**
> OrderItemDetail shopOrderItemsRetrieve()

- Admin users: full CRUD on all order items. - Non-staff users:     • list/retrieve: only items from their own orders.     • create: only if they have at least one PENDING order.     • update/partial_update: only on items whose order status == PENDING.     • delete: only on items whose order status == PENDING.

### Example

```typescript
import {
    ShopApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let id: number; //A unique integer value identifying this order item. (default to undefined)

const { status, data } = await apiInstance.shopOrderItemsRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this order item. | defaults to undefined|


### Return type

**OrderItemDetail**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Retrieve order-item |  -  |
|**201** | Create order-item |  -  |
|**400** | Validation error |  -  |
|**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopOrderItemsUpdate**
> OrderItemDetail shopOrderItemsUpdate(orderItemCreateUpdateRequest)

- Admin users: full CRUD on all order items. - Non-staff users:     • list/retrieve: only items from their own orders.     • create: only if they have at least one PENDING order.     • update/partial_update: only on items whose order status == PENDING.     • delete: only on items whose order status == PENDING.

### Example

```typescript
import {
    ShopApi,
    Configuration,
    OrderItemCreateUpdateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let id: number; //A unique integer value identifying this order item. (default to undefined)
let orderItemCreateUpdateRequest: OrderItemCreateUpdateRequest; //

const { status, data } = await apiInstance.shopOrderItemsUpdate(
    id,
    orderItemCreateUpdateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **orderItemCreateUpdateRequest** | **OrderItemCreateUpdateRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this order item. | defaults to undefined|


### Return type

**OrderItemDetail**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Retrieve order-item |  -  |
|**201** | Create order-item |  -  |
|**400** | Validation error |  -  |
|**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopOrdersCreate**
> OrderDetail shopOrdersCreate(orderCreateRequest)

- Admin users: full CRUD on all orders. - Non-staff users:     • list/retrieve: only their own orders.     • create: may create orders for themselves.     • update/partial_update: only on their own orders when status == PENDING.     • delete: only on their own orders when status == PENDING.

### Example

```typescript
import {
    ShopApi,
    Configuration,
    OrderCreateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let orderCreateRequest: OrderCreateRequest; //

const { status, data } = await apiInstance.shopOrdersCreate(
    orderCreateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **orderCreateRequest** | **OrderCreateRequest**|  | |


### Return type

**OrderDetail**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Retrieve order |  -  |
|**201** | Create order |  -  |
|**400** | Validation error |  -  |
|**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopOrdersDestroy**
> OrderDetail shopOrdersDestroy()

- Admin users: full CRUD on all orders. - Non-staff users:     • list/retrieve: only their own orders.     • create: may create orders for themselves.     • update/partial_update: only on their own orders when status == PENDING.     • delete: only on their own orders when status == PENDING.

### Example

```typescript
import {
    ShopApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let orderId: string; //A UUID string identifying this order. (default to undefined)

const { status, data } = await apiInstance.shopOrdersDestroy(
    orderId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **orderId** | [**string**] | A UUID string identifying this order. | defaults to undefined|


### Return type

**OrderDetail**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Retrieve order |  -  |
|**201** | Create order |  -  |
|**400** | Validation error |  -  |
|**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopOrdersList**
> PaginatedOrderDetailList shopOrdersList()

- Admin users: full CRUD on all orders. - Non-staff users:     • list/retrieve: only their own orders.     • create: may create orders for themselves.     • update/partial_update: only on their own orders when status == PENDING.     • delete: only on their own orders when status == PENDING.

### Example

```typescript
import {
    ShopApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let createdAfter: string; // (optional) (default to undefined)
let createdBefore: string; // (optional) (default to undefined)
let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let pageSize: number; //Number of results to return per page. (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)
let status: string; // (optional) (default to undefined)
let totalMax: number; // (optional) (default to undefined)
let totalMin: number; // (optional) (default to undefined)

const { status, data } = await apiInstance.shopOrdersList(
    createdAfter,
    createdBefore,
    ordering,
    page,
    pageSize,
    search,
    status,
    totalMax,
    totalMin
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **createdAfter** | [**string**] |  | (optional) defaults to undefined|
| **createdBefore** | [**string**] |  | (optional) defaults to undefined|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **pageSize** | [**number**] | Number of results to return per page. | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|
| **status** | [**string**] |  | (optional) defaults to undefined|
| **totalMax** | [**number**] |  | (optional) defaults to undefined|
| **totalMin** | [**number**] |  | (optional) defaults to undefined|


### Return type

**PaginatedOrderDetailList**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Retrieve order |  -  |
|**201** | Create order |  -  |
|**400** | Validation error |  -  |
|**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopOrdersPartialUpdate**
> OrderDetail shopOrdersPartialUpdate()

- Admin users: full CRUD on all orders. - Non-staff users:     • list/retrieve: only their own orders.     • create: may create orders for themselves.     • update/partial_update: only on their own orders when status == PENDING.     • delete: only on their own orders when status == PENDING.

### Example

```typescript
import {
    ShopApi,
    Configuration,
    PatchedOrderCreateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let orderId: string; //A UUID string identifying this order. (default to undefined)
let patchedOrderCreateRequest: PatchedOrderCreateRequest; // (optional)

const { status, data } = await apiInstance.shopOrdersPartialUpdate(
    orderId,
    patchedOrderCreateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedOrderCreateRequest** | **PatchedOrderCreateRequest**|  | |
| **orderId** | [**string**] | A UUID string identifying this order. | defaults to undefined|


### Return type

**OrderDetail**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Retrieve order |  -  |
|**201** | Create order |  -  |
|**400** | Validation error |  -  |
|**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopOrdersRetrieve**
> OrderDetail shopOrdersRetrieve()

- Admin users: full CRUD on all orders. - Non-staff users:     • list/retrieve: only their own orders.     • create: may create orders for themselves.     • update/partial_update: only on their own orders when status == PENDING.     • delete: only on their own orders when status == PENDING.

### Example

```typescript
import {
    ShopApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let orderId: string; //A UUID string identifying this order. (default to undefined)

const { status, data } = await apiInstance.shopOrdersRetrieve(
    orderId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **orderId** | [**string**] | A UUID string identifying this order. | defaults to undefined|


### Return type

**OrderDetail**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Retrieve order |  -  |
|**201** | Create order |  -  |
|**400** | Validation error |  -  |
|**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopOrdersUpdate**
> OrderDetail shopOrdersUpdate(orderCreateRequest)

- Admin users: full CRUD on all orders. - Non-staff users:     • list/retrieve: only their own orders.     • create: may create orders for themselves.     • update/partial_update: only on their own orders when status == PENDING.     • delete: only on their own orders when status == PENDING.

### Example

```typescript
import {
    ShopApi,
    Configuration,
    OrderCreateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let orderId: string; //A UUID string identifying this order. (default to undefined)
let orderCreateRequest: OrderCreateRequest; //

const { status, data } = await apiInstance.shopOrdersUpdate(
    orderId,
    orderCreateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **orderCreateRequest** | **OrderCreateRequest**|  | |
| **orderId** | [**string**] | A UUID string identifying this order. | defaults to undefined|


### Return type

**OrderDetail**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Retrieve order |  -  |
|**201** | Create order |  -  |
|**400** | Validation error |  -  |
|**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopProductsCreate**
> Product shopProductsCreate(productRequest)


### Example

```typescript
import {
    ShopApi,
    Configuration,
    ProductRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let productRequest: ProductRequest; //

const { status, data } = await apiInstance.shopProductsCreate(
    productRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **productRequest** | **ProductRequest**|  | |


### Return type

**Product**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Retrieve product |  -  |
|**201** | Create product |  -  |
|**400** | Validation error |  -  |
|**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopProductsDestroy**
> Product shopProductsDestroy()


### Example

```typescript
import {
    ShopApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let id: number; //A unique integer value identifying this product. (default to undefined)

const { status, data } = await apiInstance.shopProductsDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this product. | defaults to undefined|


### Return type

**Product**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Retrieve product |  -  |
|**201** | Create product |  -  |
|**400** | Validation error |  -  |
|**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopProductsList**
> PaginatedProductList shopProductsList()


### Example

```typescript
import {
    ShopApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let inStock: boolean; // (optional) (default to undefined)
let name: string; // (optional) (default to undefined)
let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let pageSize: number; //Number of results to return per page. (optional) (default to undefined)
let priceMax: number; // (optional) (default to undefined)
let priceMin: number; // (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)

const { status, data } = await apiInstance.shopProductsList(
    inStock,
    name,
    ordering,
    page,
    pageSize,
    priceMax,
    priceMin,
    search
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **inStock** | [**boolean**] |  | (optional) defaults to undefined|
| **name** | [**string**] |  | (optional) defaults to undefined|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **pageSize** | [**number**] | Number of results to return per page. | (optional) defaults to undefined|
| **priceMax** | [**number**] |  | (optional) defaults to undefined|
| **priceMin** | [**number**] |  | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|


### Return type

**PaginatedProductList**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Retrieve product |  -  |
|**201** | Create product |  -  |
|**400** | Validation error |  -  |
|**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopProductsPartialUpdate**
> Product shopProductsPartialUpdate()


### Example

```typescript
import {
    ShopApi,
    Configuration,
    PatchedProductRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let id: number; //A unique integer value identifying this product. (default to undefined)
let patchedProductRequest: PatchedProductRequest; // (optional)

const { status, data } = await apiInstance.shopProductsPartialUpdate(
    id,
    patchedProductRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedProductRequest** | **PatchedProductRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this product. | defaults to undefined|


### Return type

**Product**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Retrieve product |  -  |
|**201** | Create product |  -  |
|**400** | Validation error |  -  |
|**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopProductsRetrieve**
> Product shopProductsRetrieve()


### Example

```typescript
import {
    ShopApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let id: number; //A unique integer value identifying this product. (default to undefined)

const { status, data } = await apiInstance.shopProductsRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this product. | defaults to undefined|


### Return type

**Product**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Retrieve product |  -  |
|**201** | Create product |  -  |
|**400** | Validation error |  -  |
|**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **shopProductsUpdate**
> Product shopProductsUpdate(productRequest)


### Example

```typescript
import {
    ShopApi,
    Configuration,
    ProductRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ShopApi(configuration);

let id: number; //A unique integer value identifying this product. (default to undefined)
let productRequest: ProductRequest; //

const { status, data } = await apiInstance.shopProductsUpdate(
    id,
    productRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **productRequest** | **ProductRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this product. | defaults to undefined|


### Return type

**Product**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Retrieve product |  -  |
|**201** | Create product |  -  |
|**400** | Validation error |  -  |
|**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

