# PatchedAdminUserRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **string** |  | [optional] [default to undefined]
**username** | **string** | Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. | [optional] [default to undefined]
**first_name** | **string** |  | [optional] [default to undefined]
**last_name** | **string** |  | [optional] [default to undefined]
**password** | **string** |  | [optional] [default to undefined]
**is_active** | **boolean** | Designates whether this user should be treated as active. Unselect this instead of deleting accounts. | [optional] [default to undefined]
**is_staff** | **boolean** | Designates whether the user can log into this admin site. | [optional] [default to undefined]

## Example

```typescript
import { PatchedAdminUserRequest } from './api';

const instance: PatchedAdminUserRequest = {
    email,
    username,
    first_name,
    last_name,
    password,
    is_active,
    is_staff,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
