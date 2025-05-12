# PatchedOrderCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_id** | **string** |  | [optional] [readonly] [default to undefined]
**status** | [**StatusEnum**](StatusEnum.md) |  | [optional] [default to undefined]
**items** | [**Array&lt;OrderItemDetail&gt;**](OrderItemDetail.md) |  | [optional] [default to undefined]

## Example

```typescript
import { PatchedOrderCreate } from '@mijnorg/ecommerce-api-client';

const instance: PatchedOrderCreate = {
    order_id,
    status,
    items,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
