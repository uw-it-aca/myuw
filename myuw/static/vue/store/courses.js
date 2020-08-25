import {fetchBuilder, buildWith} from './model_builder';

const setTermAndExtractData = (response, urlExtra) => {
    let proccessValue = {};
    proccessValue[urlExtra] = response.data;
    return proccessValue;
}

const customActions = {
    fetch: fetchBuilder('/api/v1/schedule/', setTermAndExtractData, 'json'),
};

export default buildWith(
    {customActions},
);