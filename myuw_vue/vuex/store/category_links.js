import {fetchBuilder, setTermAndExtractData, buildWith} from './model_builder';

function postProcess(response, urlExtra) {
  let data = setTermAndExtractData(response, urlExtra);
  return data;
}

const customActions = {
  fetch: fetchBuilder('/api/v1/categorylinks/', postProcess, 'json'),
};

export default buildWith(
  { customActions },
);