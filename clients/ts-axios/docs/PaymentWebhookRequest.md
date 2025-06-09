# PaymentWebhookRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_id** | **string** | UUID of paid order | [default to undefined]
**status** | [**PaymentWebhookStatusEnum**](PaymentWebhookStatusEnum.md) | Payment status: \&#39;paid\&#39; or \&#39;failed\&#39;  * &#x60;paid&#x60; - paid * &#x60;failed&#x60; - failed | [default to undefined]

## Example

```typescript
import { PaymentWebhookRequest } from './api';

const instance: PaymentWebhookRequest = {
    order_id,
    status,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
