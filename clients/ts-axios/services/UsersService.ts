/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Address } from '../models/Address';
import type { AddressRequest } from '../models/AddressRequest';
import type { AdminProfile } from '../models/AdminProfile';
import type { AdminProfileRequest } from '../models/AdminProfileRequest';
import type { AdminUser } from '../models/AdminUser';
import type { AdminUserRequest } from '../models/AdminUserRequest';
import type { AppUser } from '../models/AppUser';
import type { AppUserRequest } from '../models/AppUserRequest';
import type { PaginatedAddressList } from '../models/PaginatedAddressList';
import type { PaginatedAdminProfileList } from '../models/PaginatedAdminProfileList';
import type { PaginatedAdminUserList } from '../models/PaginatedAdminUserList';
import type { PatchedAddressRequest } from '../models/PatchedAddressRequest';
import type { PatchedAdminProfileRequest } from '../models/PatchedAdminProfileRequest';
import type { PatchedAdminUserRequest } from '../models/PatchedAdminUserRequest';
import type { PatchedAppUserRequest } from '../models/PatchedAppUserRequest';
import type { PatchedUserProfileRequest } from '../models/PatchedUserProfileRequest';
import type { UserProfile } from '../models/UserProfile';
import type { UserProfileRequest } from '../models/UserProfileRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class UsersService {
    /**
     * Disable all TOTP devices for the user
     * @returns void
     * @throws ApiError
     */
    public static faDisable(): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/users/2fa/',
        });
    }
    /**
     * Generate a new TOTP device and return QR code + secret
     * @returns any
     * @throws ApiError
     */
    public static faSetup(): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/2fa/setup/',
        });
    }
    /**
     * Verify the TOTP code and confirm the device
     * @param requestBody
     * @returns void
     * @throws ApiError
     */
    public static faVerify(
        requestBody?: Record<string, any>,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/users/2fa/verify/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param city
     * @param country
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param pageSize Number of results to return per page.
     * @param search A search term.
     * @param zipcode
     * @returns PaginatedAddressList
     * @throws ApiError
     */
    public static usersAddressesList(
        city?: string,
        country?: string,
        ordering?: string,
        page?: number,
        pageSize?: number,
        search?: string,
        zipcode?: string,
    ): CancelablePromise<PaginatedAddressList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/addresses/',
            query: {
                'city': city,
                'country': country,
                'ordering': ordering,
                'page': page,
                'page_size': pageSize,
                'search': search,
                'zipcode': zipcode,
            },
        });
    }
    /**
     * @param requestBody
     * @returns Address
     * @throws ApiError
     */
    public static usersAddressesCreate(
        requestBody: AddressRequest,
    ): CancelablePromise<Address> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/users/addresses/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param id A unique integer value identifying this Address.
     * @returns Address
     * @throws ApiError
     */
    public static usersAddressesRetrieve(
        id: number,
    ): CancelablePromise<Address> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/addresses/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param id A unique integer value identifying this Address.
     * @param requestBody
     * @returns Address
     * @throws ApiError
     */
    public static usersAddressesUpdate(
        id: number,
        requestBody: AddressRequest,
    ): CancelablePromise<Address> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users/addresses/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param id A unique integer value identifying this Address.
     * @param requestBody
     * @returns Address
     * @throws ApiError
     */
    public static usersAddressesPartialUpdate(
        id: number,
        requestBody?: PatchedAddressRequest,
    ): CancelablePromise<Address> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/users/addresses/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param id A unique integer value identifying this Address.
     * @returns void
     * @throws ApiError
     */
    public static usersAddressesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/users/addresses/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Login with email+password, returns JWT + has_2fa flag
     * @param requestBody
     * @returns any
     * @throws ApiError
     */
    public static login(
        requestBody?: Record<string, any>,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/users/auth/jwt/create/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @returns AppUser
     * @throws ApiError
     */
    public static usersMeRetrieve(): CancelablePromise<AppUser> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/me/',
        });
    }
    /**
     * @param requestBody
     * @returns AppUser
     * @throws ApiError
     */
    public static usersMeUpdate(
        requestBody?: AppUserRequest,
    ): CancelablePromise<AppUser> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users/me/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param requestBody
     * @returns AppUser
     * @throws ApiError
     */
    public static usersMePartialUpdate(
        requestBody?: PatchedAppUserRequest,
    ): CancelablePromise<AppUser> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/users/me/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param city
     * @param country
     * @param isBilling
     * @param isShipping
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedAddressList
     * @throws ApiError
     */
    public static usersMeAddressesList(
        city?: string,
        country?: string,
        isBilling?: boolean,
        isShipping?: boolean,
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedAddressList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/me/addresses/',
            query: {
                'city': city,
                'country': country,
                'is_billing': isBilling,
                'is_shipping': isShipping,
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * @param requestBody
     * @returns Address
     * @throws ApiError
     */
    public static usersMeAddressesCreate(
        requestBody: AddressRequest,
    ): CancelablePromise<Address> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/users/me/addresses/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Authenticated user to GET, PATCH or DELETE their own address.
     * @param id
     * @returns Address
     * @throws ApiError
     */
    public static usersMeAddressesRetrieve(
        id: number,
    ): CancelablePromise<Address> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/me/addresses/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Authenticated user to GET, PATCH or DELETE their own address.
     * @param id
     * @param requestBody
     * @returns Address
     * @throws ApiError
     */
    public static usersMeAddressesUpdate(
        id: number,
        requestBody: AddressRequest,
    ): CancelablePromise<Address> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users/me/addresses/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Authenticated user to GET, PATCH or DELETE their own address.
     * @param id
     * @param requestBody
     * @returns Address
     * @throws ApiError
     */
    public static usersMeAddressesPartialUpdate(
        id: number,
        requestBody?: PatchedAddressRequest,
    ): CancelablePromise<Address> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/users/me/addresses/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Authenticated user to GET, PATCH or DELETE their own address.
     * @param id
     * @returns void
     * @throws ApiError
     */
    public static usersMeAddressesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/users/me/addresses/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @returns void
     * @throws ApiError
     */
    public static usersMeDeleteDestroy(): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/users/me/delete/',
        });
    }
    /**
     * @returns UserProfile
     * @throws ApiError
     */
    public static usersMeProfileRetrieve(): CancelablePromise<UserProfile> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/me/profile/',
        });
    }
    /**
     * @param requestBody
     * @returns UserProfile
     * @throws ApiError
     */
    public static usersMeProfileUpdate(
        requestBody?: UserProfileRequest,
    ): CancelablePromise<UserProfile> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users/me/profile/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param requestBody
     * @returns UserProfile
     * @throws ApiError
     */
    public static usersMeProfilePartialUpdate(
        requestBody?: PatchedUserProfileRequest,
    ): CancelablePromise<UserProfile> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/users/me/profile/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param dateOfBirth
     * @param dateOfBirthGte
     * @param dateOfBirthLte
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param phoneNumberIcontains
     * @param search A search term.
     * @param user
     * @returns PaginatedAdminProfileList
     * @throws ApiError
     */
    public static usersProfilesList(
        dateOfBirth?: string,
        dateOfBirthGte?: string,
        dateOfBirthLte?: string,
        ordering?: string,
        page?: number,
        phoneNumberIcontains?: string,
        search?: string,
        user?: number,
    ): CancelablePromise<PaginatedAdminProfileList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/profiles/',
            query: {
                'date_of_birth': dateOfBirth,
                'date_of_birth__gte': dateOfBirthGte,
                'date_of_birth__lte': dateOfBirthLte,
                'ordering': ordering,
                'page': page,
                'phone_number__icontains': phoneNumberIcontains,
                'search': search,
                'user': user,
            },
        });
    }
    /**
     * @param requestBody
     * @returns AdminProfile
     * @throws ApiError
     */
    public static usersProfilesCreate(
        requestBody: AdminProfileRequest,
    ): CancelablePromise<AdminProfile> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/users/profiles/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param id A unique integer value identifying this customer profile.
     * @returns AdminProfile
     * @throws ApiError
     */
    public static usersProfilesRetrieve(
        id: number,
    ): CancelablePromise<AdminProfile> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param id A unique integer value identifying this customer profile.
     * @param requestBody
     * @returns AdminProfile
     * @throws ApiError
     */
    public static usersProfilesUpdate(
        id: number,
        requestBody: AdminProfileRequest,
    ): CancelablePromise<AdminProfile> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users/profiles/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param id A unique integer value identifying this customer profile.
     * @param requestBody
     * @returns AdminProfile
     * @throws ApiError
     */
    public static usersProfilesPartialUpdate(
        id: number,
        requestBody?: PatchedAdminProfileRequest,
    ): CancelablePromise<AdminProfile> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/users/profiles/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param id A unique integer value identifying this customer profile.
     * @returns void
     * @throws ApiError
     */
    public static usersProfilesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/users/profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param dateJoined
     * @param email
     * @param isActive Filter on active users (true/false)
     * @param isStaff Filter on staff users (true/false)
     * @param ordering Sort by date_joined or email; prefix "-" for descending
     * @param page A page number within the paginated result set.
     * @param search Partial search on email or username
     * @returns PaginatedAdminUserList
     * @throws ApiError
     */
    public static usersUsersList(
        dateJoined?: string,
        email?: string,
        isActive?: boolean,
        isStaff?: boolean,
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedAdminUserList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/users/',
            query: {
                'date_joined': dateJoined,
                'email': email,
                'is_active': isActive,
                'is_staff': isStaff,
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * @param requestBody
     * @param isActive Filter on active users (true/false)
     * @param isStaff Filter on staff users (true/false)
     * @param ordering Sort by date_joined or email; prefix "-" for descending
     * @param search Partial search on email or username
     * @returns AdminUser
     * @throws ApiError
     */
    public static usersUsersCreate(
        requestBody: AdminUserRequest,
        isActive?: boolean,
        isStaff?: boolean,
        ordering?: string,
        search?: string,
    ): CancelablePromise<AdminUser> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/users/users/',
            query: {
                'is_active': isActive,
                'is_staff': isStaff,
                'ordering': ordering,
                'search': search,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param id A unique integer value identifying this user.
     * @param isActive Filter on active users (true/false)
     * @param isStaff Filter on staff users (true/false)
     * @param ordering Sort by date_joined or email; prefix "-" for descending
     * @param search Partial search on email or username
     * @returns AdminUser
     * @throws ApiError
     */
    public static usersUsersRetrieve(
        id: number,
        isActive?: boolean,
        isStaff?: boolean,
        ordering?: string,
        search?: string,
    ): CancelablePromise<AdminUser> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/users/{id}/',
            path: {
                'id': id,
            },
            query: {
                'is_active': isActive,
                'is_staff': isStaff,
                'ordering': ordering,
                'search': search,
            },
        });
    }
    /**
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @param isActive Filter on active users (true/false)
     * @param isStaff Filter on staff users (true/false)
     * @param ordering Sort by date_joined or email; prefix "-" for descending
     * @param search Partial search on email or username
     * @returns AdminUser
     * @throws ApiError
     */
    public static usersUsersUpdate(
        id: number,
        requestBody: AdminUserRequest,
        isActive?: boolean,
        isStaff?: boolean,
        ordering?: string,
        search?: string,
    ): CancelablePromise<AdminUser> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users/users/{id}/',
            path: {
                'id': id,
            },
            query: {
                'is_active': isActive,
                'is_staff': isStaff,
                'ordering': ordering,
                'search': search,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param id A unique integer value identifying this user.
     * @param isActive Filter on active users (true/false)
     * @param isStaff Filter on staff users (true/false)
     * @param ordering Sort by date_joined or email; prefix "-" for descending
     * @param search Partial search on email or username
     * @param requestBody
     * @returns AdminUser
     * @throws ApiError
     */
    public static usersUsersPartialUpdate(
        id: number,
        isActive?: boolean,
        isStaff?: boolean,
        ordering?: string,
        search?: string,
        requestBody?: PatchedAdminUserRequest,
    ): CancelablePromise<AdminUser> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/users/users/{id}/',
            path: {
                'id': id,
            },
            query: {
                'is_active': isActive,
                'is_staff': isStaff,
                'ordering': ordering,
                'search': search,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param id A unique integer value identifying this user.
     * @param isActive Filter on active users (true/false)
     * @param isStaff Filter on staff users (true/false)
     * @param ordering Sort by date_joined or email; prefix "-" for descending
     * @param search Partial search on email or username
     * @returns void
     * @throws ApiError
     */
    public static usersUsersDestroy(
        id: number,
        isActive?: boolean,
        isStaff?: boolean,
        ordering?: string,
        search?: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/users/users/{id}/',
            path: {
                'id': id,
            },
            query: {
                'is_active': isActive,
                'is_staff': isStaff,
                'ordering': ordering,
                'search': search,
            },
        });
    }
}
