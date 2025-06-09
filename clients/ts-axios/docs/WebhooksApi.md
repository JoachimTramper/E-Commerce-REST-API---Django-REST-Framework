# WebhooksApi

All URIs are relative to */api*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**paymentWebhook**](#paymentwebhook) | **POST** /webhooks/payment/ | |

# **paymentWebhook**
> paymentWebhook(paymentWebhookRequest)

Payment provider callback endpoint: - Verify header `X-Webhook-Key` matches the configured secret. - Expect JSON body with `order_id` (UUID) and `status` (\'paid\' or \'failed\'). - If `status == \'paid\'` and order is in `AWAITING_PAYMENT`, then:   1) Decrement `stock` and `stock_reserved` for each OrderItem within     an atomic transaction.   2) Change order status to `CONFIRMED` and save.   3) Dispatch Celery task `send_order_email_with_invoice.delay(order_id)`. - Always return 200 OK with a JSON confirmation message   `{ \'message\': \'Webhook received\' }`.

### Example

```typescript
import {
    WebhooksApi,
    Configuration,
    PaymentWebhookRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new WebhooksApi(configuration);

let xWebhookKey: string; //Secret key required to authenticate the webhook request (default to undefined)
let paymentWebhookRequest: PaymentWebhookRequest; //

const { status, data } = await apiInstance.paymentWebhook(
    xWebhookKey,
    paymentWebhookRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **paymentWebhookRequest** | **PaymentWebhookRequest**|  | |
| **xWebhookKey** | [**string**] | Secret key required to authenticate the webhook request | defaults to undefined|


### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Webhook received; if status&#x3D;\&#39;paid\&#39; and order was AWAITING_PAYMENT, stock is decremented, order set to CONFIRMED, and invoice email triggered. |  -  |
|**400** | Missing data or insufficient stock |  -  |
|**403** | Unauthorized (invalid X-Webhook-Key) |  -  |
|**404** | Order not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

