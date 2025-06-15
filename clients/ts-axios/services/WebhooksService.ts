/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PaymentWebhookRequest } from '../models/PaymentWebhookRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class WebhooksService {
    /**
     * Payment provider callback endpoint:
     * - Verify header `X-Webhook-Key` matches the configured secret.
     * - Expect JSON body with `order_id` (UUID) and `status` ('paid' or 'failed').
     * - If `status == 'paid'` and order is in `AWAITING_PAYMENT`, then:
     * 1) Decrement `stock` and `stock_reserved` for each OrderItem within     an atomic transaction.
     * 2) Change order status to `CONFIRMED` and save.
     * 3) Dispatch Celery task `send_order_email_with_invoice.delay(order_id)`.
     * - Always return 200 OK with a JSON confirmation message   `{ 'message': 'Webhook received' }`.
     * @param xWebhookKey Secret key required to authenticate the webhook request
     * @param requestBody
     * @returns any Webhook received; if status='paid' and order was AWAITING_PAYMENT, stock is decremented, order set to CONFIRMED, and invoice email triggered.
     * @throws ApiError
     */
    public static paymentWebhook(
        xWebhookKey: string,
        requestBody: PaymentWebhookRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/webhooks/payment/',
            headers: {
                'X-Webhook-Key': xWebhookKey,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Missing data or insufficient stock`,
                403: `Unauthorized (invalid X-Webhook-Key)`,
                404: `Order not found`,
            },
        });
    }
}
