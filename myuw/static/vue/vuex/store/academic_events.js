import dayjs from 'dayjs';
import {fetchBuilder, extractData, buildWith} from './model_builder';

const postProccess = (response) => {
  let data = extractData(response);

  data.forEach((event) => {
    event.start = dayjs(event.start);
    event.end = dayjs(event.end);
    event.year = String(event.year);
  });

  return data;
}

const customActions = {
  fetch: fetchBuilder('/api/v1/academic_events/', postProccess, 'json'),
};

export default buildWith(
  {customActions},
);
