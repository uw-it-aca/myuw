import {fetchBuilder, extractData, buildWith} from './model_builder';
import {
  parseDate,
} from './common';

const postProccess = (response, urlExtra) => {
  let data = {};
  data[urlExtra] = extractData(response);

  data[urlExtra].forEach((event) => {
    event.start = parseDate(event.start);
    event.end = parseDate(event.end);
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
