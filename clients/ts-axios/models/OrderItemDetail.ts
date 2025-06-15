/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Product } from './Product';
export type OrderItemDetail = {
    readonly id: number;
    readonly order: string;
    readonly product: Product;
    quantity: number;
    readonly item_subtotal: number;
};

