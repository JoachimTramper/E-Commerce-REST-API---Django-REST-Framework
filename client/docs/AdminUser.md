# AdminUser


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**email** | **string** |  | [default to undefined]
**username** | **string** | Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. | [default to undefined]
**first_name** | **string** |  | [optional] [default to undefined]
**last_name** | **string** |  | [optional] [default to undefined]
**is_active** | **boolean** | Designates whether this user should be treated as active. Unselect this instead of deleting accounts. | [optional] [default to undefined]
**is_staff** | **boolean** | Designates whether the user can log into this admin site. | [optional] [default to undefined]

## Example

```typescript
import { AdminUser } from './api';

const instance: AdminUser = {
    id,
    email,
    username,
    first_name,
    last_name,
    is_active,
    is_staff,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
