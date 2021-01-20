import {fetchBuilder, buildWith, setTermAndExtractData} from './model_builder';

const customActions = {
  fetch: fetchBuilder('/api/v1/academic_events', setTermAndExtractData, 'json'),
};

export default buildWith(
  { customActions },
);