# UsersApi

All URIs are relative to */api*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**_2faDisable**](#_2fadisable) | **DELETE** /users/2fa/ | |
|[**_2faSetup**](#_2fasetup) | **GET** /users/2fa/setup/ | |
|[**_2faVerify**](#_2faverify) | **POST** /users/2fa/verify/ | |
|[**login**](#login) | **POST** /users/auth/jwt/create/ | |
|[**usersAddressesCreate**](#usersaddressescreate) | **POST** /users/addresses/ | |
|[**usersAddressesDestroy**](#usersaddressesdestroy) | **DELETE** /users/addresses/{id}/ | |
|[**usersAddressesList**](#usersaddresseslist) | **GET** /users/addresses/ | |
|[**usersAddressesPartialUpdate**](#usersaddressespartialupdate) | **PATCH** /users/addresses/{id}/ | |
|[**usersAddressesRetrieve**](#usersaddressesretrieve) | **GET** /users/addresses/{id}/ | |
|[**usersAddressesUpdate**](#usersaddressesupdate) | **PUT** /users/addresses/{id}/ | |
|[**usersMeAddressesCreate**](#usersmeaddressescreate) | **POST** /users/me/addresses/ | |
|[**usersMeAddressesDestroy**](#usersmeaddressesdestroy) | **DELETE** /users/me/addresses/{id}/ | |
|[**usersMeAddressesList**](#usersmeaddresseslist) | **GET** /users/me/addresses/ | |
|[**usersMeAddressesPartialUpdate**](#usersmeaddressespartialupdate) | **PATCH** /users/me/addresses/{id}/ | |
|[**usersMeAddressesRetrieve**](#usersmeaddressesretrieve) | **GET** /users/me/addresses/{id}/ | |
|[**usersMeAddressesUpdate**](#usersmeaddressesupdate) | **PUT** /users/me/addresses/{id}/ | |
|[**usersMeDeleteDestroy**](#usersmedeletedestroy) | **DELETE** /users/me/delete/ | |
|[**usersMePartialUpdate**](#usersmepartialupdate) | **PATCH** /users/me/ | |
|[**usersMeProfilePartialUpdate**](#usersmeprofilepartialupdate) | **PATCH** /users/me/profile/ | |
|[**usersMeProfileRetrieve**](#usersmeprofileretrieve) | **GET** /users/me/profile/ | |
|[**usersMeProfileUpdate**](#usersmeprofileupdate) | **PUT** /users/me/profile/ | |
|[**usersMeRetrieve**](#usersmeretrieve) | **GET** /users/me/ | |
|[**usersMeUpdate**](#usersmeupdate) | **PUT** /users/me/ | |
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

# **_2faDisable**
> _2faDisable()

Disable all TOTP devices for the user

### Example

```typescript
import {
    UsersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

const { status, data } = await apiInstance._2faDisable();
```

### Parameters
This endpoint does not have any parameters.


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

# **_2faSetup**
> { [key: string]: any; } _2faSetup()

Generate a new TOTP device and return QR code + secret

### Example

```typescript
import {
    UsersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

const { status, data } = await apiInstance._2faSetup();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**{ [key: string]: any; }**

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

# **_2faVerify**
> _2faVerify()

Verify the TOTP code and confirm the device

### Example

```typescript
import {
    UsersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let requestBody: { [key: string]: any; }; // (optional)

const { status, data } = await apiInstance._2faVerify(
    requestBody
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **requestBody** | **{ [key: string]: any; }**|  | |


### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth), [jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**204** | No response body |  -  |
|**400** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **login**
> { [key: string]: any; } login()

Login with email+password, returns JWT + has_2fa flag

### Example

```typescript
import {
    UsersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let requestBody: { [key: string]: any; }; // (optional)

const { status, data } = await apiInstance.login(
    requestBody
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **requestBody** | **{ [key: string]: any; }**|  | |


### Return type

**{ [key: string]: any; }**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**401** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **usersAddressesCreate**
> Address usersAddressesCreate(addressRequest)


### Example

```typescript
import {
    UsersApi,
    Configuration,
    AddressRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let addressRequest: AddressRequest; //

const { status, data } = await apiInstance.usersAddressesCreate(
    addressRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **addressRequest** | **AddressRequest**|  | |


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
} from './api';

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
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let city: string; // (optional) (default to undefined)
let country: string; // (optional) (default to undefined)
let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let pageSize: number; //Number of results to return per page. (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)
let zipcode: string; // (optional) (default to undefined)

const { status, data } = await apiInstance.usersAddressesList(
    city,
    country,
    ordering,
    page,
    pageSize,
    search,
    zipcode
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **city** | [**string**] |  | (optional) defaults to undefined|
| **country** | [**string**] |  | (optional) defaults to undefined|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **pageSize** | [**number**] | Number of results to return per page. | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|
| **zipcode** | [**string**] |  | (optional) defaults to undefined|


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
    PatchedAddressRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this Address. (default to undefined)
let patchedAddressRequest: PatchedAddressRequest; // (optional)

const { status, data } = await apiInstance.usersAddressesPartialUpdate(
    id,
    patchedAddressRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedAddressRequest** | **PatchedAddressRequest**|  | |
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
} from './api';

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
> Address usersAddressesUpdate(addressRequest)


### Example

```typescript
import {
    UsersApi,
    Configuration,
    AddressRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this Address. (default to undefined)
let addressRequest: AddressRequest; //

const { status, data } = await apiInstance.usersAddressesUpdate(
    id,
    addressRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **addressRequest** | **AddressRequest**|  | |
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

# **usersMeAddressesCreate**
> Address usersMeAddressesCreate(addressRequest)


### Example

```typescript
import {
    UsersApi,
    Configuration,
    AddressRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let addressRequest: AddressRequest; //

const { status, data } = await apiInstance.usersMeAddressesCreate(
    addressRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **addressRequest** | **AddressRequest**|  | |


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

# **usersMeAddressesDestroy**
> usersMeAddressesDestroy()

Authenticated user to GET, PATCH or DELETE their own address.

### Example

```typescript
import {
    UsersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; // (default to undefined)

const { status, data } = await apiInstance.usersMeAddressesDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] |  | defaults to undefined|


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

# **usersMeAddressesList**
> PaginatedAddressList usersMeAddressesList()


### Example

```typescript
import {
    UsersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let city: string; // (optional) (default to undefined)
let country: string; // (optional) (default to undefined)
let isBilling: boolean; // (optional) (default to undefined)
let isShipping: boolean; // (optional) (default to undefined)
let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)

const { status, data } = await apiInstance.usersMeAddressesList(
    city,
    country,
    isBilling,
    isShipping,
    ordering,
    page,
    search
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **city** | [**string**] |  | (optional) defaults to undefined|
| **country** | [**string**] |  | (optional) defaults to undefined|
| **isBilling** | [**boolean**] |  | (optional) defaults to undefined|
| **isShipping** | [**boolean**] |  | (optional) defaults to undefined|
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

# **usersMeAddressesPartialUpdate**
> Address usersMeAddressesPartialUpdate()

Authenticated user to GET, PATCH or DELETE their own address.

### Example

```typescript
import {
    UsersApi,
    Configuration,
    PatchedAddressRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; // (default to undefined)
let patchedAddressRequest: PatchedAddressRequest; // (optional)

const { status, data } = await apiInstance.usersMeAddressesPartialUpdate(
    id,
    patchedAddressRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedAddressRequest** | **PatchedAddressRequest**|  | |
| **id** | [**number**] |  | defaults to undefined|


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

# **usersMeAddressesRetrieve**
> Address usersMeAddressesRetrieve()

Authenticated user to GET, PATCH or DELETE their own address.

### Example

```typescript
import {
    UsersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; // (default to undefined)

const { status, data } = await apiInstance.usersMeAddressesRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] |  | defaults to undefined|


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

# **usersMeAddressesUpdate**
> Address usersMeAddressesUpdate(addressRequest)

Authenticated user to GET, PATCH or DELETE their own address.

### Example

```typescript
import {
    UsersApi,
    Configuration,
    AddressRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; // (default to undefined)
let addressRequest: AddressRequest; //

const { status, data } = await apiInstance.usersMeAddressesUpdate(
    id,
    addressRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **addressRequest** | **AddressRequest**|  | |
| **id** | [**number**] |  | defaults to undefined|


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

# **usersMeDeleteDestroy**
> usersMeDeleteDestroy()


### Example

```typescript
import {
    UsersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

const { status, data } = await apiInstance.usersMeDeleteDestroy();
```

### Parameters
This endpoint does not have any parameters.


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

# **usersMePartialUpdate**
> AppUser usersMePartialUpdate()


### Example

```typescript
import {
    UsersApi,
    Configuration,
    PatchedAppUserRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let patchedAppUserRequest: PatchedAppUserRequest; // (optional)

const { status, data } = await apiInstance.usersMePartialUpdate(
    patchedAppUserRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedAppUserRequest** | **PatchedAppUserRequest**|  | |


### Return type

**AppUser**

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

# **usersMeProfilePartialUpdate**
> UserProfile usersMeProfilePartialUpdate()


### Example

```typescript
import {
    UsersApi,
    Configuration,
    PatchedUserProfileRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let patchedUserProfileRequest: PatchedUserProfileRequest; // (optional)

const { status, data } = await apiInstance.usersMeProfilePartialUpdate(
    patchedUserProfileRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedUserProfileRequest** | **PatchedUserProfileRequest**|  | |


### Return type

**UserProfile**

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

# **usersMeProfileRetrieve**
> UserProfile usersMeProfileRetrieve()


### Example

```typescript
import {
    UsersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

const { status, data } = await apiInstance.usersMeProfileRetrieve();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**UserProfile**

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

# **usersMeProfileUpdate**
> UserProfile usersMeProfileUpdate()


### Example

```typescript
import {
    UsersApi,
    Configuration,
    UserProfileRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let userProfileRequest: UserProfileRequest; // (optional)

const { status, data } = await apiInstance.usersMeProfileUpdate(
    userProfileRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **userProfileRequest** | **UserProfileRequest**|  | |


### Return type

**UserProfile**

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

# **usersMeRetrieve**
> AppUser usersMeRetrieve()


### Example

```typescript
import {
    UsersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

const { status, data } = await apiInstance.usersMeRetrieve();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**AppUser**

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

# **usersMeUpdate**
> AppUser usersMeUpdate()


### Example

```typescript
import {
    UsersApi,
    Configuration,
    AppUserRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let appUserRequest: AppUserRequest; // (optional)

const { status, data } = await apiInstance.usersMeUpdate(
    appUserRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **appUserRequest** | **AppUserRequest**|  | |


### Return type

**AppUser**

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
> AdminProfile usersProfilesCreate(adminProfileRequest)


### Example

```typescript
import {
    UsersApi,
    Configuration,
    AdminProfileRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let adminProfileRequest: AdminProfileRequest; //

const { status, data } = await apiInstance.usersProfilesCreate(
    adminProfileRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **adminProfileRequest** | **AdminProfileRequest**|  | |


### Return type

**AdminProfile**

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
} from './api';

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
> PaginatedAdminProfileList usersProfilesList()


### Example

```typescript
import {
    UsersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let dateOfBirth: string; // (optional) (default to undefined)
let dateOfBirthGte: string; // (optional) (default to undefined)
let dateOfBirthLte: string; // (optional) (default to undefined)
let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let phoneNumberIcontains: string; // (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)
let user: number; // (optional) (default to undefined)

const { status, data } = await apiInstance.usersProfilesList(
    dateOfBirth,
    dateOfBirthGte,
    dateOfBirthLte,
    ordering,
    page,
    phoneNumberIcontains,
    search,
    user
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **dateOfBirth** | [**string**] |  | (optional) defaults to undefined|
| **dateOfBirthGte** | [**string**] |  | (optional) defaults to undefined|
| **dateOfBirthLte** | [**string**] |  | (optional) defaults to undefined|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **phoneNumberIcontains** | [**string**] |  | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|
| **user** | [**number**] |  | (optional) defaults to undefined|


### Return type

**PaginatedAdminProfileList**

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
> AdminProfile usersProfilesPartialUpdate()


### Example

```typescript
import {
    UsersApi,
    Configuration,
    PatchedAdminProfileRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this customer profile. (default to undefined)
let patchedAdminProfileRequest: PatchedAdminProfileRequest; // (optional)

const { status, data } = await apiInstance.usersProfilesPartialUpdate(
    id,
    patchedAdminProfileRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedAdminProfileRequest** | **PatchedAdminProfileRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this customer profile. | defaults to undefined|


### Return type

**AdminProfile**

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
> AdminProfile usersProfilesRetrieve()


### Example

```typescript
import {
    UsersApi,
    Configuration
} from './api';

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

**AdminProfile**

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
> AdminProfile usersProfilesUpdate(adminProfileRequest)


### Example

```typescript
import {
    UsersApi,
    Configuration,
    AdminProfileRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this customer profile. (default to undefined)
let adminProfileRequest: AdminProfileRequest; //

const { status, data } = await apiInstance.usersProfilesUpdate(
    id,
    adminProfileRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **adminProfileRequest** | **AdminProfileRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this customer profile. | defaults to undefined|


### Return type

**AdminProfile**

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
> AdminUser usersUsersCreate(adminUserRequest)


### Example

```typescript
import {
    UsersApi,
    Configuration,
    AdminUserRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let adminUserRequest: AdminUserRequest; //
let isActive: boolean; //Filter on active users (true/false) (optional) (default to undefined)
let isStaff: boolean; //Filter on staff users (true/false) (optional) (default to undefined)
let ordering: string; //Sort by date_joined or email; prefix \"-\" for descending (optional) (default to undefined)
let search: string; //Partial search on email or username (optional) (default to undefined)

const { status, data } = await apiInstance.usersUsersCreate(
    adminUserRequest,
    isActive,
    isStaff,
    ordering,
    search
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **adminUserRequest** | **AdminUserRequest**|  | |
| **isActive** | [**boolean**] | Filter on active users (true/false) | (optional) defaults to undefined|
| **isStaff** | [**boolean**] | Filter on staff users (true/false) | (optional) defaults to undefined|
| **ordering** | [**string**] | Sort by date_joined or email; prefix \&quot;-\&quot; for descending | (optional) defaults to undefined|
| **search** | [**string**] | Partial search on email or username | (optional) defaults to undefined|


### Return type

**AdminUser**

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
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)
let isActive: boolean; //Filter on active users (true/false) (optional) (default to undefined)
let isStaff: boolean; //Filter on staff users (true/false) (optional) (default to undefined)
let ordering: string; //Sort by date_joined or email; prefix \"-\" for descending (optional) (default to undefined)
let search: string; //Partial search on email or username (optional) (default to undefined)

const { status, data } = await apiInstance.usersUsersDestroy(
    id,
    isActive,
    isStaff,
    ordering,
    search
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|
| **isActive** | [**boolean**] | Filter on active users (true/false) | (optional) defaults to undefined|
| **isStaff** | [**boolean**] | Filter on staff users (true/false) | (optional) defaults to undefined|
| **ordering** | [**string**] | Sort by date_joined or email; prefix \&quot;-\&quot; for descending | (optional) defaults to undefined|
| **search** | [**string**] | Partial search on email or username | (optional) defaults to undefined|


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
> PaginatedAdminUserList usersUsersList()


### Example

```typescript
import {
    UsersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let dateJoined: string; // (optional) (default to undefined)
let email: string; // (optional) (default to undefined)
let isActive: boolean; //Filter on active users (true/false) (optional) (default to undefined)
let isStaff: boolean; //Filter on staff users (true/false) (optional) (default to undefined)
let ordering: string; //Sort by date_joined or email; prefix \"-\" for descending (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let search: string; //Partial search on email or username (optional) (default to undefined)

const { status, data } = await apiInstance.usersUsersList(
    dateJoined,
    email,
    isActive,
    isStaff,
    ordering,
    page,
    search
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **dateJoined** | [**string**] |  | (optional) defaults to undefined|
| **email** | [**string**] |  | (optional) defaults to undefined|
| **isActive** | [**boolean**] | Filter on active users (true/false) | (optional) defaults to undefined|
| **isStaff** | [**boolean**] | Filter on staff users (true/false) | (optional) defaults to undefined|
| **ordering** | [**string**] | Sort by date_joined or email; prefix \&quot;-\&quot; for descending | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **search** | [**string**] | Partial search on email or username | (optional) defaults to undefined|


### Return type

**PaginatedAdminUserList**

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
> AdminUser usersUsersPartialUpdate()


### Example

```typescript
import {
    UsersApi,
    Configuration,
    PatchedAdminUserRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)
let isActive: boolean; //Filter on active users (true/false) (optional) (default to undefined)
let isStaff: boolean; //Filter on staff users (true/false) (optional) (default to undefined)
let ordering: string; //Sort by date_joined or email; prefix \"-\" for descending (optional) (default to undefined)
let search: string; //Partial search on email or username (optional) (default to undefined)
let patchedAdminUserRequest: PatchedAdminUserRequest; // (optional)

const { status, data } = await apiInstance.usersUsersPartialUpdate(
    id,
    isActive,
    isStaff,
    ordering,
    search,
    patchedAdminUserRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedAdminUserRequest** | **PatchedAdminUserRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|
| **isActive** | [**boolean**] | Filter on active users (true/false) | (optional) defaults to undefined|
| **isStaff** | [**boolean**] | Filter on staff users (true/false) | (optional) defaults to undefined|
| **ordering** | [**string**] | Sort by date_joined or email; prefix \&quot;-\&quot; for descending | (optional) defaults to undefined|
| **search** | [**string**] | Partial search on email or username | (optional) defaults to undefined|


### Return type

**AdminUser**

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
> AdminUser usersUsersRetrieve()


### Example

```typescript
import {
    UsersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)
let isActive: boolean; //Filter on active users (true/false) (optional) (default to undefined)
let isStaff: boolean; //Filter on staff users (true/false) (optional) (default to undefined)
let ordering: string; //Sort by date_joined or email; prefix \"-\" for descending (optional) (default to undefined)
let search: string; //Partial search on email or username (optional) (default to undefined)

const { status, data } = await apiInstance.usersUsersRetrieve(
    id,
    isActive,
    isStaff,
    ordering,
    search
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|
| **isActive** | [**boolean**] | Filter on active users (true/false) | (optional) defaults to undefined|
| **isStaff** | [**boolean**] | Filter on staff users (true/false) | (optional) defaults to undefined|
| **ordering** | [**string**] | Sort by date_joined or email; prefix \&quot;-\&quot; for descending | (optional) defaults to undefined|
| **search** | [**string**] | Partial search on email or username | (optional) defaults to undefined|


### Return type

**AdminUser**

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
> AdminUser usersUsersUpdate(adminUserRequest)


### Example

```typescript
import {
    UsersApi,
    Configuration,
    AdminUserRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)
let adminUserRequest: AdminUserRequest; //
let isActive: boolean; //Filter on active users (true/false) (optional) (default to undefined)
let isStaff: boolean; //Filter on staff users (true/false) (optional) (default to undefined)
let ordering: string; //Sort by date_joined or email; prefix \"-\" for descending (optional) (default to undefined)
let search: string; //Partial search on email or username (optional) (default to undefined)

const { status, data } = await apiInstance.usersUsersUpdate(
    id,
    adminUserRequest,
    isActive,
    isStaff,
    ordering,
    search
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **adminUserRequest** | **AdminUserRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|
| **isActive** | [**boolean**] | Filter on active users (true/false) | (optional) defaults to undefined|
| **isStaff** | [**boolean**] | Filter on staff users (true/false) | (optional) defaults to undefined|
| **ordering** | [**string**] | Sort by date_joined or email; prefix \&quot;-\&quot; for descending | (optional) defaults to undefined|
| **search** | [**string**] | Partial search on email or username | (optional) defaults to undefined|


### Return type

**AdminUser**

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

