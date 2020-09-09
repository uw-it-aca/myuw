import {fetchBuilder, extractData, buildWith} from './model_builder';

const customActions = {
    fetch: fetchBuilder('/api/v1/hx_toolkit/', extractData, 'text'),
};

export default buildWith(
    {customActions},
);
