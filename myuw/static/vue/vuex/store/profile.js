import {fetchBuilder, extractData, buildWith} from './model_builder';

const customActions = {
    fetch: fetchBuilder('/api/v1/profile/', extractData, 'json'),
};

export default buildWith(
    {customActions},
);
