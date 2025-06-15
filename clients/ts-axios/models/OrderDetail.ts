/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OrderItemDetail } from './OrderItemDetail';
import type { Status93bEnum } from './Status93bEnum';
export type OrderDetail = {
    readonly order_id: string;
    readonly order_number: number;
    readonly created_at: string;
    readonly status: Status93bEnum;
    items: Array<OrderItemDetail>;
    readonly total_amount: number;
};

