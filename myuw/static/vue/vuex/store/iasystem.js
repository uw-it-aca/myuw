import {fetchBuilder, extractData, buildWith} from './model_builder';

const customActions = {
    fetch: fetchBuilder('/api/v1/ias/', extractData, 'json'),
};

export default buildWith(
    {customActions},
);
