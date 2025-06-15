/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type Address = {
    readonly id: number;
    /**
     * e.g. 'Home', 'Work'
     */
    label: string;
    street: string;
    number: string;
    zipcode: string;
    city: string;
    country: string;
    is_billing?: boolean;
    is_shipping?: boolean;
};

