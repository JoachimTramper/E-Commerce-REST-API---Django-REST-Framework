/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PaymentWebhookStatusEnum } from './PaymentWebhookStatusEnum';
export type PaymentWebhookRequest = {
    /**
     * UUID of paid order
     */
    order_id: string;
    /**
     * Payment status: 'paid' or 'failed'
     *
     * * `paid` - paid
     * * `failed` - failed
     */
    status: PaymentWebhookStatusEnum;
};

