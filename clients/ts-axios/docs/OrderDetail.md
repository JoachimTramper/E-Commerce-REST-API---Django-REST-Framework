# OrderDetail


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_id** | **string** |  | [readonly] [default to undefined]
**order_number** | **number** |  | [readonly] [default to undefined]
**created_at** | **string** |  | [readonly] [default to undefined]
**status** | [**StatusEnum**](StatusEnum.md) |  | [readonly] [default to undefined]
**items** | [**Array&lt;OrderItemDetail&gt;**](OrderItemDetail.md) |  | [default to undefined]
**total_amount** | **number** |  | [readonly] [default to undefined]

## Example

```typescript
import { OrderDetail } from '@mijnorg/ecommerce-api-client';

const instance: OrderDetail = {
    order_id,
    order_number,
    created_at,
    status,
    items,
    total_amount,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
