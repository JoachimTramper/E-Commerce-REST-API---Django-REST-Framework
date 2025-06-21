# UserProfile


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**phone_number** | **string** |  | [optional] [default to undefined]
**date_of_birth** | **string** |  | [optional] [default to undefined]
**addresses** | [**Array&lt;Address&gt;**](Address.md) |  | [readonly] [default to undefined]

## Example

```typescript
import { UserProfile } from './api';

const instance: UserProfile = {
    id,
    phone_number,
    date_of_birth,
    addresses,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
