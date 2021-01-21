import {fetchBuilder, extractData, buildWith} from './model_builder';

function postProcess(response) {
  const data = response.data;
  if (data.tuition_accbalance.match(' CR')) {
    data.tuition_accbalance = -1 * parseFloat(data.tuition_accbalance.replace(' CR', ''));
  } else {
    data.tuition_accbalance = parseFloat(data.tuition_accbalance);
  }
  data.pce_accbalance = parseFloat(data.pce_accbalance);

  return data;
};

const customActions = {
  fetch: fetchBuilder('/api/v1/finance/', postProcess, 'json'),
};

export default buildWith(
  {customActions}
);