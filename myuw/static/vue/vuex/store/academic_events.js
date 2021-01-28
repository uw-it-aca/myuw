import {fetchBuilder, extractData, buildWith} from './model_builder';
import {
  strToDate,
} from './common';

const postProccess = (response) => {
  let data = extractData(response);

  data.forEach((event) => {
    event.start = strToDate(event.start);
    event.end = strToDate(event.end);
    event.year = String(event.year);
    event.label = event.year + ' '+ event.quarter + ', ' + event.summary;
  });

  return data;
}

const customActions = {
  fetch: fetchBuilder('/api/v1/academic_events/', postProccess, 'json'),
};

export default buildWith(
  {customActions},
);
