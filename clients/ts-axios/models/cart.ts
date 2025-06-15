/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OrderItemDetail } from './OrderItemDetail';
export type Cart = {
    readonly order_id: string;
    readonly created_at: string;
    readonly items: Array<OrderItemDetail>;
    readonly total_amount: number;
};

