/* Class to simplify message passing to service workers. */

export enum QueryType {
    GET_CACHEDIDS, // Request all IDs of books within the cache. Param: int[]
}

export interface QueryObjectI {
    query_type: QueryType;
    query_param: any;
}

export class QueryObject implements QueryObjectI {
    constructor(
        public query_type: QueryType, 
        public query_param: any,
        ){ }
}