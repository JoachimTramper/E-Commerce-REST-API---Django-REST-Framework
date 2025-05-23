/* tslint:disable */
/* eslint-disable */
/**
 * ECOMMERCE-API
 * REST API for managing products, orders, order items, user accounts and authentication 
 *
 * The version of the OpenAPI document: 1.0.0
 * Contact: joachimtramper@gmail.com
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */



/**
 * 
 * @export
 * @interface TokenObtainPair
 */
export interface TokenObtainPair {
    /**
     * 
     * @type {string}
     * @memberof TokenObtainPair
     */
    'email': string;
    /**
     * 
     * @type {string}
     * @memberof TokenObtainPair
     */
    'password': string;
    /**
     * 
     * @type {string}
     * @memberof TokenObtainPair
     */
    'access': string;
    /**
     * 
     * @type {string}
     * @memberof TokenObtainPair
     */
    'refresh': string;
}

