import dayjs from 'dayjs';

import {fetchBuilder, setTermAndExtractData, buildWith} from './model_builder';

const customActions = {
  fetch: fetchBuilder(
    '/api/v1/instructor_schedule/',
    setTermAndExtractData,
    'json'
  ),
};

export default buildWith(
  { customActions },
);
