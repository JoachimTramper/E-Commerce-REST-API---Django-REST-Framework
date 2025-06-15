/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Address } from './Address';
export type UserProfile = {
    readonly id: number;
    phone_number?: string;
    date_of_birth?: string | null;
    readonly addresses: Array<Address>;
};

