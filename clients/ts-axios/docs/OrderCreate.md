# OrderCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_id** | **string** |  | [readonly] [default to undefined]
**status** | [**Status93bEnum**](Status93bEnum.md) |  | [optional] [default to undefined]
**items** | [**Array&lt;OrderItemDetail&gt;**](OrderItemDetail.md) |  | [default to undefined]

## Example

```typescript
import { OrderCreate } from './api';

const instance: OrderCreate = {
    order_id,
    status,
    items,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
