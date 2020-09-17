import {fetchBuilder, setTermAndExtractData, buildWith} from './model_builder';

const customActions = {
    fetch: fetchBuilder('/api/v1/schedule/', setTermAndExtractData, 'json'),
};

export default buildWith(
    {customActions},
);