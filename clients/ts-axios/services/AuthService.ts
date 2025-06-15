/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Activation } from '../models/Activation';
import type { ActivationRequest } from '../models/ActivationRequest';
import type { AppUser } from '../models/AppUser';
import type { AppUserRequest } from '../models/AppUserRequest';
import type { PaginatedAppUserList } from '../models/PaginatedAppUserList';
import type { PasswordResetConfirmRetype } from '../models/PasswordResetConfirmRetype';
import type { PasswordResetConfirmRetypeRequest } from '../models/PasswordResetConfirmRetypeRequest';
import type { PatchedAppUserRequest } from '../models/PatchedAppUserRequest';
import type { SendEmailReset } from '../models/SendEmailReset';
import type { SendEmailResetRequest } from '../models/SendEmailResetRequest';
import type { SetPassword } from '../models/SetPassword';
import type { SetPasswordRequest } from '../models/SetPasswordRequest';
import type { SetUsername } from '../models/SetUsername';
import type { SetUsernameRequest } from '../models/SetUsernameRequest';
import type { TokenObtainPair } from '../models/TokenObtainPair';
import type { TokenObtainPairRequest } from '../models/TokenObtainPairRequest';
import type { TokenRefresh } from '../models/TokenRefresh';
import type { TokenRefreshRequest } from '../models/TokenRefreshRequest';
import type { TokenVerifyRequest } from '../models/TokenVerifyRequest';
import type { UserCreatePasswordRetype } from '../models/UserCreatePasswordRetype';
import type { UserCreatePasswordRetypeRequest } from '../models/UserCreatePasswordRetypeRequest';
import type { UsernameResetConfirm } from '../models/UsernameResetConfirm';
import type { UsernameResetConfirmRequest } from '../models/UsernameResetConfirmRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class AuthService {
    /**
     * Takes a set of user credentials and returns an access and refresh JSON web
     * token pair to prove the authentication of those credentials.
     * @param requestBody
     * @returns TokenObtainPair
     * @throws ApiError
     */
    public static authJwtCreateCreate(
        requestBody: TokenObtainPairRequest,
    ): CancelablePromise<TokenObtainPair> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/jwt/create/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Takes a refresh type JSON web token and returns an access type JSON web
     * token if the refresh token is valid.
     * @param requestBody
     * @returns TokenRefresh
     * @throws ApiError
     */
    public static authJwtRefreshCreate(
        requestBody: TokenRefreshRequest,
    ): CancelablePromise<TokenRefresh> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/jwt/refresh/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Takes a token and indicates if it is valid.  This view provides no
     * information about a token's fitness for a particular use.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public static authJwtVerifyCreate(
        requestBody: TokenVerifyRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/jwt/verify/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedAppUserList
     * @throws ApiError
     */
    public static authUsersList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedAppUserList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/auth/users/',
            query: {
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * @param requestBody
     * @returns UserCreatePasswordRetype
     * @throws ApiError
     */
    public static authUsersCreate(
        requestBody: UserCreatePasswordRetypeRequest,
    ): CancelablePromise<UserCreatePasswordRetype> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/users/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param id A unique integer value identifying this user.
     * @returns AppUser
     * @throws ApiError
     */
    public static authUsersRetrieve(
        id: number,
    ): CancelablePromise<AppUser> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/auth/users/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns AppUser
     * @throws ApiError
     */
    public static authUsersUpdate(
        id: number,
        requestBody?: AppUserRequest,
    ): CancelablePromise<AppUser> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/auth/users/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns AppUser
     * @throws ApiError
     */
    public static authUsersPartialUpdate(
        id: number,
        requestBody?: PatchedAppUserRequest,
    ): CancelablePromise<AppUser> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/auth/users/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param id A unique integer value identifying this user.
     * @returns void
     * @throws ApiError
     */
    public static authUsersDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/auth/users/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param requestBody
     * @returns Activation
     * @throws ApiError
     */
    public static authUsersActivationCreate(
        requestBody: ActivationRequest,
    ): CancelablePromise<Activation> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/users/activation/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @returns AppUser
     * @throws ApiError
     */
    public static authUsersMeRetrieve(): CancelablePromise<AppUser> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/auth/users/me/',
        });
    }
    /**
     * @param requestBody
     * @returns AppUser
     * @throws ApiError
     */
    public static authUsersMeUpdate(
        requestBody?: AppUserRequest,
    ): CancelablePromise<AppUser> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/auth/users/me/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param requestBody
     * @returns AppUser
     * @throws ApiError
     */
    public static authUsersMePartialUpdate(
        requestBody?: PatchedAppUserRequest,
    ): CancelablePromise<AppUser> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/auth/users/me/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @returns void
     * @throws ApiError
     */
    public static authUsersMeDestroy(): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/auth/users/me/',
        });
    }
    /**
     * @param requestBody
     * @returns SendEmailReset
     * @throws ApiError
     */
    public static authUsersResendActivationCreate(
        requestBody: SendEmailResetRequest,
    ): CancelablePromise<SendEmailReset> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/users/resend_activation/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param requestBody
     * @returns SendEmailReset
     * @throws ApiError
     */
    public static authUsersResetEmailCreate(
        requestBody: SendEmailResetRequest,
    ): CancelablePromise<SendEmailReset> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/users/reset_email/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param requestBody
     * @returns UsernameResetConfirm
     * @throws ApiError
     */
    public static authUsersResetEmailConfirmCreate(
        requestBody: UsernameResetConfirmRequest,
    ): CancelablePromise<UsernameResetConfirm> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/users/reset_email_confirm/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param requestBody
     * @returns SendEmailReset
     * @throws ApiError
     */
    public static authUsersResetPasswordCreate(
        requestBody: SendEmailResetRequest,
    ): CancelablePromise<SendEmailReset> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/users/reset_password/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param requestBody
     * @returns PasswordResetConfirmRetype
     * @throws ApiError
     */
    public static authUsersResetPasswordConfirmCreate(
        requestBody: PasswordResetConfirmRetypeRequest,
    ): CancelablePromise<PasswordResetConfirmRetype> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/users/reset_password_confirm/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param requestBody
     * @returns SetUsername
     * @throws ApiError
     */
    public static authUsersSetEmailCreate(
        requestBody: SetUsernameRequest,
    ): CancelablePromise<SetUsername> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/users/set_email/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param requestBody
     * @returns SetPassword
     * @throws ApiError
     */
    public static authUsersSetPasswordCreate(
        requestBody: SetPasswordRequest,
    ): CancelablePromise<SetPassword> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/users/set_password/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
}
