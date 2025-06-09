# AuthApi

All URIs are relative to */api*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**authJwtCreateCreate**](#authjwtcreatecreate) | **POST** /auth/jwt/create/ | |
|[**authJwtRefreshCreate**](#authjwtrefreshcreate) | **POST** /auth/jwt/refresh/ | |
|[**authJwtVerifyCreate**](#authjwtverifycreate) | **POST** /auth/jwt/verify/ | |
|[**authUsersActivationCreate**](#authusersactivationcreate) | **POST** /auth/users/activation/ | |
|[**authUsersCreate**](#authuserscreate) | **POST** /auth/users/ | |
|[**authUsersDestroy**](#authusersdestroy) | **DELETE** /auth/users/{id}/ | |
|[**authUsersList**](#authuserslist) | **GET** /auth/users/ | |
|[**authUsersMeDestroy**](#authusersmedestroy) | **DELETE** /auth/users/me/ | |
|[**authUsersMePartialUpdate**](#authusersmepartialupdate) | **PATCH** /auth/users/me/ | |
|[**authUsersMeRetrieve**](#authusersmeretrieve) | **GET** /auth/users/me/ | |
|[**authUsersMeUpdate**](#authusersmeupdate) | **PUT** /auth/users/me/ | |
|[**authUsersPartialUpdate**](#authuserspartialupdate) | **PATCH** /auth/users/{id}/ | |
|[**authUsersResendActivationCreate**](#authusersresendactivationcreate) | **POST** /auth/users/resend_activation/ | |
|[**authUsersResetEmailConfirmCreate**](#authusersresetemailconfirmcreate) | **POST** /auth/users/reset_email_confirm/ | |
|[**authUsersResetEmailCreate**](#authusersresetemailcreate) | **POST** /auth/users/reset_email/ | |
|[**authUsersResetPasswordConfirmCreate**](#authusersresetpasswordconfirmcreate) | **POST** /auth/users/reset_password_confirm/ | |
|[**authUsersResetPasswordCreate**](#authusersresetpasswordcreate) | **POST** /auth/users/reset_password/ | |
|[**authUsersRetrieve**](#authusersretrieve) | **GET** /auth/users/{id}/ | |
|[**authUsersSetEmailCreate**](#authuserssetemailcreate) | **POST** /auth/users/set_email/ | |
|[**authUsersSetPasswordCreate**](#authuserssetpasswordcreate) | **POST** /auth/users/set_password/ | |
|[**authUsersUpdate**](#authusersupdate) | **PUT** /auth/users/{id}/ | |

# **authJwtCreateCreate**
> TokenObtainPair authJwtCreateCreate(tokenObtainPairRequest)

Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials.

### Example

```typescript
import {
    AuthApi,
    Configuration,
    TokenObtainPairRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let tokenObtainPairRequest: TokenObtainPairRequest; //

const { status, data } = await apiInstance.authJwtCreateCreate(
    tokenObtainPairRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **tokenObtainPairRequest** | **TokenObtainPairRequest**|  | |


### Return type

**TokenObtainPair**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **authJwtRefreshCreate**
> TokenRefresh authJwtRefreshCreate(tokenRefreshRequest)

Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid.

### Example

```typescript
import {
    AuthApi,
    Configuration,
    TokenRefreshRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let tokenRefreshRequest: TokenRefreshRequest; //

const { status, data } = await apiInstance.authJwtRefreshCreate(
    tokenRefreshRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **tokenRefreshRequest** | **TokenRefreshRequest**|  | |


### Return type

**TokenRefresh**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **authJwtVerifyCreate**
> authJwtVerifyCreate(tokenVerifyRequest)

Takes a token and indicates if it is valid.  This view provides no information about a token\'s fitness for a particular use.

### Example

```typescript
import {
    AuthApi,
    Configuration,
    TokenVerifyRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let tokenVerifyRequest: TokenVerifyRequest; //

const { status, data } = await apiInstance.authJwtVerifyCreate(
    tokenVerifyRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **tokenVerifyRequest** | **TokenVerifyRequest**|  | |


### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **authUsersActivationCreate**
> Activation authUsersActivationCreate(activationRequest)


### Example

```typescript
import {
    AuthApi,
    Configuration,
    ActivationRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let activationRequest: ActivationRequest; //

const { status, data } = await apiInstance.authUsersActivationCreate(
    activationRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **activationRequest** | **ActivationRequest**|  | |


### Return type

**Activation**

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

# **authUsersCreate**
> UserCreatePasswordRetype authUsersCreate(userCreatePasswordRetypeRequest)


### Example

```typescript
import {
    AuthApi,
    Configuration,
    UserCreatePasswordRetypeRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let userCreatePasswordRetypeRequest: UserCreatePasswordRetypeRequest; //

const { status, data } = await apiInstance.authUsersCreate(
    userCreatePasswordRetypeRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **userCreatePasswordRetypeRequest** | **UserCreatePasswordRetypeRequest**|  | |


### Return type

**UserCreatePasswordRetype**

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

# **authUsersDestroy**
> authUsersDestroy()


### Example

```typescript
import {
    AuthApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)

const { status, data } = await apiInstance.authUsersDestroy(
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

# **authUsersList**
> PaginatedAppUserList authUsersList()


### Example

```typescript
import {
    AuthApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)

const { status, data } = await apiInstance.authUsersList(
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

**PaginatedAppUserList**

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

# **authUsersMeDestroy**
> authUsersMeDestroy()


### Example

```typescript
import {
    AuthApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

const { status, data } = await apiInstance.authUsersMeDestroy();
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

# **authUsersMePartialUpdate**
> AppUser authUsersMePartialUpdate()


### Example

```typescript
import {
    AuthApi,
    Configuration,
    PatchedAppUserRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let patchedAppUserRequest: PatchedAppUserRequest; // (optional)

const { status, data } = await apiInstance.authUsersMePartialUpdate(
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

# **authUsersMeRetrieve**
> AppUser authUsersMeRetrieve()


### Example

```typescript
import {
    AuthApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

const { status, data } = await apiInstance.authUsersMeRetrieve();
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

# **authUsersMeUpdate**
> AppUser authUsersMeUpdate()


### Example

```typescript
import {
    AuthApi,
    Configuration,
    AppUserRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let appUserRequest: AppUserRequest; // (optional)

const { status, data } = await apiInstance.authUsersMeUpdate(
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

# **authUsersPartialUpdate**
> AppUser authUsersPartialUpdate()


### Example

```typescript
import {
    AuthApi,
    Configuration,
    PatchedAppUserRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)
let patchedAppUserRequest: PatchedAppUserRequest; // (optional)

const { status, data } = await apiInstance.authUsersPartialUpdate(
    id,
    patchedAppUserRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedAppUserRequest** | **PatchedAppUserRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|


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

# **authUsersResendActivationCreate**
> SendEmailReset authUsersResendActivationCreate(sendEmailResetRequest)


### Example

```typescript
import {
    AuthApi,
    Configuration,
    SendEmailResetRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let sendEmailResetRequest: SendEmailResetRequest; //

const { status, data } = await apiInstance.authUsersResendActivationCreate(
    sendEmailResetRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **sendEmailResetRequest** | **SendEmailResetRequest**|  | |


### Return type

**SendEmailReset**

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

# **authUsersResetEmailConfirmCreate**
> UsernameResetConfirm authUsersResetEmailConfirmCreate(usernameResetConfirmRequest)


### Example

```typescript
import {
    AuthApi,
    Configuration,
    UsernameResetConfirmRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let usernameResetConfirmRequest: UsernameResetConfirmRequest; //

const { status, data } = await apiInstance.authUsersResetEmailConfirmCreate(
    usernameResetConfirmRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **usernameResetConfirmRequest** | **UsernameResetConfirmRequest**|  | |


### Return type

**UsernameResetConfirm**

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

# **authUsersResetEmailCreate**
> SendEmailReset authUsersResetEmailCreate(sendEmailResetRequest)


### Example

```typescript
import {
    AuthApi,
    Configuration,
    SendEmailResetRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let sendEmailResetRequest: SendEmailResetRequest; //

const { status, data } = await apiInstance.authUsersResetEmailCreate(
    sendEmailResetRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **sendEmailResetRequest** | **SendEmailResetRequest**|  | |


### Return type

**SendEmailReset**

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

# **authUsersResetPasswordConfirmCreate**
> PasswordResetConfirmRetype authUsersResetPasswordConfirmCreate(passwordResetConfirmRetypeRequest)


### Example

```typescript
import {
    AuthApi,
    Configuration,
    PasswordResetConfirmRetypeRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let passwordResetConfirmRetypeRequest: PasswordResetConfirmRetypeRequest; //

const { status, data } = await apiInstance.authUsersResetPasswordConfirmCreate(
    passwordResetConfirmRetypeRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **passwordResetConfirmRetypeRequest** | **PasswordResetConfirmRetypeRequest**|  | |


### Return type

**PasswordResetConfirmRetype**

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

# **authUsersResetPasswordCreate**
> SendEmailReset authUsersResetPasswordCreate(sendEmailResetRequest)


### Example

```typescript
import {
    AuthApi,
    Configuration,
    SendEmailResetRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let sendEmailResetRequest: SendEmailResetRequest; //

const { status, data } = await apiInstance.authUsersResetPasswordCreate(
    sendEmailResetRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **sendEmailResetRequest** | **SendEmailResetRequest**|  | |


### Return type

**SendEmailReset**

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

# **authUsersRetrieve**
> AppUser authUsersRetrieve()


### Example

```typescript
import {
    AuthApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)

const { status, data } = await apiInstance.authUsersRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|


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

# **authUsersSetEmailCreate**
> SetUsername authUsersSetEmailCreate(setUsernameRequest)


### Example

```typescript
import {
    AuthApi,
    Configuration,
    SetUsernameRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let setUsernameRequest: SetUsernameRequest; //

const { status, data } = await apiInstance.authUsersSetEmailCreate(
    setUsernameRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **setUsernameRequest** | **SetUsernameRequest**|  | |


### Return type

**SetUsername**

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

# **authUsersSetPasswordCreate**
> SetPassword authUsersSetPasswordCreate(setPasswordRequest)


### Example

```typescript
import {
    AuthApi,
    Configuration,
    SetPasswordRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let setPasswordRequest: SetPasswordRequest; //

const { status, data } = await apiInstance.authUsersSetPasswordCreate(
    setPasswordRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **setPasswordRequest** | **SetPasswordRequest**|  | |


### Return type

**SetPassword**

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

# **authUsersUpdate**
> AppUser authUsersUpdate()


### Example

```typescript
import {
    AuthApi,
    Configuration,
    AppUserRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)
let appUserRequest: AppUserRequest; // (optional)

const { status, data } = await apiInstance.authUsersUpdate(
    id,
    appUserRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **appUserRequest** | **AppUserRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|


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

