import {extractData, buildWith} from './model_builder';

export default buildWith(
    '/api/v1/applications/',
    extractData,
);
