# Address


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**label** | **string** | e.g. \&#39;Home\&#39;, \&#39;Work\&#39; | [default to undefined]
**street** | **string** |  | [default to undefined]
**number** | **string** |  | [default to undefined]
**zipcode** | **string** |  | [default to undefined]
**city** | **string** |  | [default to undefined]
**country** | **string** |  | [default to undefined]
**is_billing** | **boolean** |  | [optional] [default to undefined]
**is_shipping** | **boolean** |  | [optional] [default to undefined]
**profile** | **number** |  | [default to undefined]

## Example

```typescript
import { Address } from '@mijnorg/ecommerce-api-client';

const instance: Address = {
    id,
    label,
    street,
    number,
    zipcode,
    city,
    country,
    is_billing,
    is_shipping,
    profile,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
