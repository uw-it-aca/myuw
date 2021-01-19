import {fetchBuilder, buildWith, extractData} from './model_builder';

const customActions = {
  fetch: fetchBuilder('/api/v1/academic_events/current/', extractData, 'json'),
};

export default buildWith(
  { customActions },
);