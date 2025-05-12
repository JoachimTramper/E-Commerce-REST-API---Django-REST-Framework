# UsersApi

All URIs are relative to */api*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**usersAddressesCreate**](#usersaddressescreate) | **POST** /users/addresses/ | |
|[**usersAddressesDestroy**](#usersaddressesdestroy) | **DELETE** /users/addresses/{id}/ | |
|[**usersAddressesList**](#usersaddresseslist) | **GET** /users/addresses/ | |
|[**usersAddressesPartialUpdate**](#usersaddressespartialupdate) | **PATCH** /users/addresses/{id}/ | |
|[**usersAddressesRetrieve**](#usersaddressesretrieve) | **GET** /users/addresses/{id}/ | |
|[**usersAddressesUpdate**](#usersaddressesupdate) | **PUT** /users/addresses/{id}/ | |
|[**usersProfilesCreate**](#usersprofilescreate) | **POST** /users/profiles/ | |
|[**usersProfilesDestroy**](#usersprofilesdestroy) | **DELETE** /users/profiles/{id}/ | |
|[**usersProfilesList**](#usersprofileslist) | **GET** /users/profiles/ | |
|[**usersProfilesPartialUpdate**](#usersprofilespartialupdate) | **PATCH** /users/profiles/{id}/ | |
|[**usersProfilesRetrieve**](#usersprofilesretrieve) | **GET** /users/profiles/{id}/ | |
|[**usersProfilesUpdate**](#usersprofilesupdate) | **PUT** /users/profiles/{id}/ | |
|[**usersUsersCreate**](#usersuserscreate) | **POST** /users/users/ | |
|[**usersUsersDestroy**](#usersusersdestroy) | **DELETE** /users/users/{id}/ | |
|[**usersUsersList**](#usersuserslist) | **GET** /users/users/ | |
|[**usersUsersPartialUpdate**](#usersuserspartialupdate) | **PATCH** /users/users/{id}/ | |
|[**usersUsersRetrieve**](#usersusersretrieve) | **GET** /users/users/{id}/ | |
|[**usersUsersUpdate**](#usersusersupdate) | **PUT** /users/users/{id}/ | |

# **usersAddressesCreate**
> Address usersAddressesCreate(address)


### Example

```typescript
import {
    UsersApi,
    Configuration,
    Address
} from '@mijnorg/ecommerce-api-client';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let address: Address; //

const { status, data } = await apiInstance.usersAddressesCreate(
    address
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **address** | **Address**|  | |


### Return type

**Address**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **usersAddressesDestroy**
> usersAddressesDestroy()


### Example

```typescript
import {
    UsersApi,
    Configuration
} from '@mijnorg/ecommerce-api-client';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this Address. (default to undefined)

const { status, data } = await apiInstance.usersAddressesDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Address. | defaults to undefined|


### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **usersAddressesList**
> PaginatedAddressList usersAddressesList()


### Example

```typescript
import {
    UsersApi,
    Configuration
} from '@mijnorg/ecommerce-api-client';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)

const { status, data } = await apiInstance.usersAddressesList(
    ordering,
    page,
    search
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|


### Return type

**PaginatedAddressList**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **usersAddressesPartialUpdate**
> Address usersAddressesPartialUpdate()


### Example

```typescript
import {
    UsersApi,
    Configuration,
    PatchedAddress
} from '@mijnorg/ecommerce-api-client';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this Address. (default to undefined)
let patchedAddress: PatchedAddress; // (optional)

const { status, data } = await apiInstance.usersAddressesPartialUpdate(
    id,
    patchedAddress
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedAddress** | **PatchedAddress**|  | |
| **id** | [**number**] | A unique integer value identifying this Address. | defaults to undefined|


### Return type

**Address**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **usersAddressesRetrieve**
> Address usersAddressesRetrieve()


### Example

```typescript
import {
    UsersApi,
    Configuration
} from '@mijnorg/ecommerce-api-client';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this Address. (default to undefined)

const { status, data } = await apiInstance.usersAddressesRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Address. | defaults to undefined|


### Return type

**Address**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **usersAddressesUpdate**
> Address usersAddressesUpdate(address)


### Example

```typescript
import {
    UsersApi,
    Configuration,
    Address
} from '@mijnorg/ecommerce-api-client';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this Address. (default to undefined)
let address: Address; //

const { status, data } = await apiInstance.usersAddressesUpdate(
    id,
    address
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **address** | **Address**|  | |
| **id** | [**number**] | A unique integer value identifying this Address. | defaults to undefined|


### Return type

**Address**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **usersProfilesCreate**
> CustomerProfile usersProfilesCreate(customerProfile)


### Example

```typescript
import {
    UsersApi,
    Configuration,
    CustomerProfile
} from '@mijnorg/ecommerce-api-client';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let customerProfile: CustomerProfile; //

const { status, data } = await apiInstance.usersProfilesCreate(
    customerProfile
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **customerProfile** | **CustomerProfile**|  | |


### Return type

**CustomerProfile**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **usersProfilesDestroy**
> usersProfilesDestroy()


### Example

```typescript
import {
    UsersApi,
    Configuration
} from '@mijnorg/ecommerce-api-client';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this customer profile. (default to undefined)

const { status, data } = await apiInstance.usersProfilesDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this customer profile. | defaults to undefined|


### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **usersProfilesList**
> PaginatedCustomerProfileList usersProfilesList()


### Example

```typescript
import {
    UsersApi,
    Configuration
} from '@mijnorg/ecommerce-api-client';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)

const { status, data } = await apiInstance.usersProfilesList(
    ordering,
    page,
    search
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|


### Return type

**PaginatedCustomerProfileList**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **usersProfilesPartialUpdate**
> CustomerProfile usersProfilesPartialUpdate()


### Example

```typescript
import {
    UsersApi,
    Configuration,
    PatchedCustomerProfile
} from '@mijnorg/ecommerce-api-client';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this customer profile. (default to undefined)
let patchedCustomerProfile: PatchedCustomerProfile; // (optional)

const { status, data } = await apiInstance.usersProfilesPartialUpdate(
    id,
    patchedCustomerProfile
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedCustomerProfile** | **PatchedCustomerProfile**|  | |
| **id** | [**number**] | A unique integer value identifying this customer profile. | defaults to undefined|


### Return type

**CustomerProfile**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **usersProfilesRetrieve**
> CustomerProfile usersProfilesRetrieve()


### Example

```typescript
import {
    UsersApi,
    Configuration
} from '@mijnorg/ecommerce-api-client';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this customer profile. (default to undefined)

const { status, data } = await apiInstance.usersProfilesRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this customer profile. | defaults to undefined|


### Return type

**CustomerProfile**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **usersProfilesUpdate**
> CustomerProfile usersProfilesUpdate(customerProfile)


### Example

```typescript
import {
    UsersApi,
    Configuration,
    CustomerProfile
} from '@mijnorg/ecommerce-api-client';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this customer profile. (default to undefined)
let customerProfile: CustomerProfile; //

const { status, data } = await apiInstance.usersProfilesUpdate(
    id,
    customerProfile
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **customerProfile** | **CustomerProfile**|  | |
| **id** | [**number**] | A unique integer value identifying this customer profile. | defaults to undefined|


### Return type

**CustomerProfile**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **usersUsersCreate**
> User usersUsersCreate(user)


### Example

```typescript
import {
    UsersApi,
    Configuration,
    User
} from '@mijnorg/ecommerce-api-client';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let user: User; //

const { status, data } = await apiInstance.usersUsersCreate(
    user
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **user** | **User**|  | |


### Return type

**User**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **usersUsersDestroy**
> usersUsersDestroy()


### Example

```typescript
import {
    UsersApi,
    Configuration
} from '@mijnorg/ecommerce-api-client';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)

const { status, data } = await apiInstance.usersUsersDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|


### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **usersUsersList**
> PaginatedUserList usersUsersList()


### Example

```typescript
import {
    UsersApi,
    Configuration
} from '@mijnorg/ecommerce-api-client';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)

const { status, data } = await apiInstance.usersUsersList(
    ordering,
    page,
    search
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|


### Return type

**PaginatedUserList**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **usersUsersPartialUpdate**
> User usersUsersPartialUpdate()


### Example

```typescript
import {
    UsersApi,
    Configuration,
    PatchedUser
} from '@mijnorg/ecommerce-api-client';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)
let patchedUser: PatchedUser; // (optional)

const { status, data } = await apiInstance.usersUsersPartialUpdate(
    id,
    patchedUser
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedUser** | **PatchedUser**|  | |
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|


### Return type

**User**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **usersUsersRetrieve**
> User usersUsersRetrieve()


### Example

```typescript
import {
    UsersApi,
    Configuration
} from '@mijnorg/ecommerce-api-client';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)

const { status, data } = await apiInstance.usersUsersRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|


### Return type

**User**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **usersUsersUpdate**
> User usersUsersUpdate(user)


### Example

```typescript
import {
    UsersApi,
    Configuration,
    User
} from '@mijnorg/ecommerce-api-client';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)
let user: User; //

const { status, data } = await apiInstance.usersUsersUpdate(
    id,
    user
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **user** | **User**|  | |
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|


### Return type

**User**

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

