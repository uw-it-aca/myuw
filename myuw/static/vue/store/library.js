import {extractData, buildWith} from './model_builder';

export default buildWith(
    '/api/v1/library/',
    extractData,
);
