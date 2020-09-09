import {fetchBuilder, extractData, buildWith} from './model_builder';

const postProccess = (response, urlExtra) => {
    let proccessValue = {};
    proccessValue[urlExtra] = response.data;
    return proccessValue;
}

const customActions = {
    fetch: fetchBuilder('/api/v1/hx_toolkit/', postProccess, 'text'),
};

export default buildWith(
    {customActions},
);
