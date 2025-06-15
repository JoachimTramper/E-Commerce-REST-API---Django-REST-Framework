/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OrderItemDetail } from './OrderItemDetail';
import type { Status93bEnum } from './Status93bEnum';
export type OrderCreate = {
    readonly order_id: string;
    status?: Status93bEnum;
    items: Array<OrderItemDetail>;
};

