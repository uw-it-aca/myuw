import {fetchBuilder, extractData, buildWith} from './model_builder';

const customActions = {
    fetch: fetchBuilder('/api/v1/idcard-elig/', extractData, 'json'),
};

export default buildWith(
    {customActions},
);