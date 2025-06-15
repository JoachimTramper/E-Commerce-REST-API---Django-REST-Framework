/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OrderItemDetailRequest } from './OrderItemDetailRequest';
import type { Status93bEnum } from './Status93bEnum';
export type PatchedOrderCreateRequest = {
    status?: Status93bEnum;
    items?: Array<OrderItemDetailRequest>;
};

