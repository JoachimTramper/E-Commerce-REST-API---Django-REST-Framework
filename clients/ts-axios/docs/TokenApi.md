# TokenApi

All URIs are relative to *https://web-production-7c555.up.railway.app/api*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**tokenCreate**](#tokencreate) | **POST** /token/ | |
|[**tokenRefreshCreate**](#tokenrefreshcreate) | **POST** /token/refresh/ | |

# **tokenCreate**
> TokenObtainPair tokenCreate(tokenObtainPairRequest)

Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials.

### Example

```typescript
import {
    TokenApi,
    Configuration,
    TokenObtainPairRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new TokenApi(configuration);

let tokenObtainPairRequest: TokenObtainPairRequest; //

const { status, data } = await apiInstance.tokenCreate(
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

# **tokenRefreshCreate**
> TokenRefresh tokenRefreshCreate(tokenRefreshRequest)

Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid.

### Example

```typescript
import {
    TokenApi,
    Configuration,
    TokenRefreshRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new TokenApi(configuration);

let tokenRefreshRequest: TokenRefreshRequest; //

const { status, data } = await apiInstance.tokenRefreshCreate(
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

