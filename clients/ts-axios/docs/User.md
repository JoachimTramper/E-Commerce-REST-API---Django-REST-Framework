# User


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**email** | **string** |  | [default to undefined]
**first_name** | **string** |  | [optional] [default to undefined]
**last_name** | **string** |  | [optional] [default to undefined]
**profile** | [**CustomerProfile**](CustomerProfile.md) |  | [readonly] [default to undefined]

## Example

```typescript
import { User } from '@mijnorg/ecommerce-api-client';

const instance: User = {
    id,
    email,
    first_name,
    last_name,
    profile,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
