# OrderItemDetail


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**order** | **string** |  | [readonly] [default to undefined]
**product** | [**Product**](Product.md) |  | [readonly] [default to undefined]
**product_id** | **number** |  | [default to undefined]
**quantity** | **number** |  | [default to undefined]
**item_subtotal** | **number** |  | [readonly] [default to undefined]

## Example

```typescript
import { OrderItemDetail } from '@mijnorg/ecommerce-api-client';

const instance: OrderItemDetail = {
    id,
    order,
    product,
    product_id,
    quantity,
    item_subtotal,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
