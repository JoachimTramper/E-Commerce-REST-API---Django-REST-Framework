## @mijnorg/ecommerce-api-client@1.0.0

This generator creates TypeScript/JavaScript client that utilizes [axios](https://github.com/axios/axios). The generated Node module can be used in the following environments:

Environment
* Node.js
* Webpack
* Browserify

Language level
* ES5 - you must have a Promises/A+ library installed
* ES6

Module system
* CommonJS
* ES6 module system

It can be used in both TypeScript and JavaScript. In TypeScript, the definition will be automatically resolved via `package.json`. ([Reference](https://www.typescriptlang.org/docs/handbook/declaration-files/consumption.html))

### Building

To build and compile the typescript sources to javascript use:
```
npm install
npm run build
```

### Publishing

First build the package then run `npm publish`

### Consuming

navigate to the folder of your consuming project and run one of the following commands.

_published:_

```
npm install @mijnorg/ecommerce-api-client@1.0.0 --save
```

_unPublished (not recommended):_

```
npm install PATH_TO_GENERATED_PACKAGE --save
```

### Documentation for API Endpoints

All URIs are relative to */api*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*ShopApi* | [**cartItemCreate**](docs/ShopApi.md#cartitemcreate) | **POST** /shop/cart/items/ | 
*ShopApi* | [**cartItemsList**](docs/ShopApi.md#cartitemslist) | **GET** /shop/cart/items/ | 
*ShopApi* | [**cartItemsRetrieve**](docs/ShopApi.md#cartitemsretrieve) | **GET** /shop/cart/items/{id}/ | 
*ShopApi* | [**shopCartItemsDestroy**](docs/ShopApi.md#shopcartitemsdestroy) | **DELETE** /shop/cart/items/{id}/ | 
*ShopApi* | [**shopCartItemsPartialUpdate**](docs/ShopApi.md#shopcartitemspartialupdate) | **PATCH** /shop/cart/items/{id}/ | 
*ShopApi* | [**shopCartItemsUpdate**](docs/ShopApi.md#shopcartitemsupdate) | **PUT** /shop/cart/items/{id}/ | 
*ShopApi* | [**shopCartList**](docs/ShopApi.md#shopcartlist) | **GET** /shop/cart/ | 
*ShopApi* | [**shopOrderItemsCreate**](docs/ShopApi.md#shoporderitemscreate) | **POST** /shop/order-items/ | 
*ShopApi* | [**shopOrderItemsDestroy**](docs/ShopApi.md#shoporderitemsdestroy) | **DELETE** /shop/order-items/{id}/ | 
*ShopApi* | [**shopOrderItemsList**](docs/ShopApi.md#shoporderitemslist) | **GET** /shop/order-items/ | 
*ShopApi* | [**shopOrderItemsPartialUpdate**](docs/ShopApi.md#shoporderitemspartialupdate) | **PATCH** /shop/order-items/{id}/ | 
*ShopApi* | [**shopOrderItemsRetrieve**](docs/ShopApi.md#shoporderitemsretrieve) | **GET** /shop/order-items/{id}/ | 
*ShopApi* | [**shopOrderItemsUpdate**](docs/ShopApi.md#shoporderitemsupdate) | **PUT** /shop/order-items/{id}/ | 
*ShopApi* | [**shopOrdersCheckoutCreate**](docs/ShopApi.md#shoporderscheckoutcreate) | **POST** /shop/orders/{order_id}/checkout/ | 
*ShopApi* | [**shopOrdersCreate**](docs/ShopApi.md#shoporderscreate) | **POST** /shop/orders/ | 
*ShopApi* | [**shopOrdersDestroy**](docs/ShopApi.md#shopordersdestroy) | **DELETE** /shop/orders/{order_id}/ | 
*ShopApi* | [**shopOrdersList**](docs/ShopApi.md#shoporderslist) | **GET** /shop/orders/ | 
*ShopApi* | [**shopOrdersPartialUpdate**](docs/ShopApi.md#shoporderspartialupdate) | **PATCH** /shop/orders/{order_id}/ | 
*ShopApi* | [**shopOrdersRetrieve**](docs/ShopApi.md#shopordersretrieve) | **GET** /shop/orders/{order_id}/ | 
*ShopApi* | [**shopOrdersUpdate**](docs/ShopApi.md#shopordersupdate) | **PUT** /shop/orders/{order_id}/ | 
*ShopApi* | [**shopProductsCreate**](docs/ShopApi.md#shopproductscreate) | **POST** /shop/products/ | 
*ShopApi* | [**shopProductsDestroy**](docs/ShopApi.md#shopproductsdestroy) | **DELETE** /shop/products/{id}/ | 
*ShopApi* | [**shopProductsList**](docs/ShopApi.md#shopproductslist) | **GET** /shop/products/ | 
*ShopApi* | [**shopProductsPartialUpdate**](docs/ShopApi.md#shopproductspartialupdate) | **PATCH** /shop/products/{id}/ | 
*ShopApi* | [**shopProductsRetrieve**](docs/ShopApi.md#shopproductsretrieve) | **GET** /shop/products/{id}/ | 
*ShopApi* | [**shopProductsUpdate**](docs/ShopApi.md#shopproductsupdate) | **PUT** /shop/products/{id}/ | 
*TokenApi* | [**tokenCreate**](docs/TokenApi.md#tokencreate) | **POST** /token/ | 
*TokenApi* | [**tokenRefreshCreate**](docs/TokenApi.md#tokenrefreshcreate) | **POST** /token/refresh/ | 
*UsersApi* | [**usersAddressesCreate**](docs/UsersApi.md#usersaddressescreate) | **POST** /users/addresses/ | 
*UsersApi* | [**usersAddressesDestroy**](docs/UsersApi.md#usersaddressesdestroy) | **DELETE** /users/addresses/{id}/ | 
*UsersApi* | [**usersAddressesList**](docs/UsersApi.md#usersaddresseslist) | **GET** /users/addresses/ | 
*UsersApi* | [**usersAddressesPartialUpdate**](docs/UsersApi.md#usersaddressespartialupdate) | **PATCH** /users/addresses/{id}/ | 
*UsersApi* | [**usersAddressesRetrieve**](docs/UsersApi.md#usersaddressesretrieve) | **GET** /users/addresses/{id}/ | 
*UsersApi* | [**usersAddressesUpdate**](docs/UsersApi.md#usersaddressesupdate) | **PUT** /users/addresses/{id}/ | 
*UsersApi* | [**usersProfilesCreate**](docs/UsersApi.md#usersprofilescreate) | **POST** /users/profiles/ | 
*UsersApi* | [**usersProfilesDestroy**](docs/UsersApi.md#usersprofilesdestroy) | **DELETE** /users/profiles/{id}/ | 
*UsersApi* | [**usersProfilesList**](docs/UsersApi.md#usersprofileslist) | **GET** /users/profiles/ | 
*UsersApi* | [**usersProfilesPartialUpdate**](docs/UsersApi.md#usersprofilespartialupdate) | **PATCH** /users/profiles/{id}/ | 
*UsersApi* | [**usersProfilesRetrieve**](docs/UsersApi.md#usersprofilesretrieve) | **GET** /users/profiles/{id}/ | 
*UsersApi* | [**usersProfilesUpdate**](docs/UsersApi.md#usersprofilesupdate) | **PUT** /users/profiles/{id}/ | 
*UsersApi* | [**usersUsersCreate**](docs/UsersApi.md#usersuserscreate) | **POST** /users/users/ | 
*UsersApi* | [**usersUsersDestroy**](docs/UsersApi.md#usersusersdestroy) | **DELETE** /users/users/{id}/ | 
*UsersApi* | [**usersUsersList**](docs/UsersApi.md#usersuserslist) | **GET** /users/users/ | 
*UsersApi* | [**usersUsersPartialUpdate**](docs/UsersApi.md#usersuserspartialupdate) | **PATCH** /users/users/{id}/ | 
*UsersApi* | [**usersUsersRetrieve**](docs/UsersApi.md#usersusersretrieve) | **GET** /users/users/{id}/ | 
*UsersApi* | [**usersUsersUpdate**](docs/UsersApi.md#usersusersupdate) | **PUT** /users/users/{id}/ | 


### Documentation For Models

 - [Address](docs/Address.md)
 - [Cart](docs/Cart.md)
 - [CustomerProfile](docs/CustomerProfile.md)
 - [OrderCreate](docs/OrderCreate.md)
 - [OrderDetail](docs/OrderDetail.md)
 - [OrderItemCreateUpdate](docs/OrderItemCreateUpdate.md)
 - [OrderItemDetail](docs/OrderItemDetail.md)
 - [OrderItemList](docs/OrderItemList.md)
 - [PaginatedAddressList](docs/PaginatedAddressList.md)
 - [PaginatedCustomerProfileList](docs/PaginatedCustomerProfileList.md)
 - [PaginatedOrderCreateList](docs/PaginatedOrderCreateList.md)
 - [PaginatedOrderDetailList](docs/PaginatedOrderDetailList.md)
 - [PaginatedOrderItemDetailList](docs/PaginatedOrderItemDetailList.md)
 - [PaginatedOrderItemListList](docs/PaginatedOrderItemListList.md)
 - [PaginatedProductList](docs/PaginatedProductList.md)
 - [PaginatedUserList](docs/PaginatedUserList.md)
 - [PatchedAddress](docs/PatchedAddress.md)
 - [PatchedCustomerProfile](docs/PatchedCustomerProfile.md)
 - [PatchedOrderCreate](docs/PatchedOrderCreate.md)
 - [PatchedOrderItemCreateUpdate](docs/PatchedOrderItemCreateUpdate.md)
 - [PatchedProduct](docs/PatchedProduct.md)
 - [PatchedUser](docs/PatchedUser.md)
 - [Product](docs/Product.md)
 - [StatusEnum](docs/StatusEnum.md)
 - [TokenObtainPair](docs/TokenObtainPair.md)
 - [TokenRefresh](docs/TokenRefresh.md)
 - [User](docs/User.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization


Authentication schemes defined for the API:
<a id="cookieAuth"></a>
### cookieAuth

- **Type**: API key
- **API key parameter name**: sessionid
- **Location**: 

<a id="jwtAuth"></a>
### jwtAuth

- **Type**: Bearer authentication (JWT)

