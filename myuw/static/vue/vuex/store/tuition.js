import {fetchBuilder, extractData, buildWith} from './model_builder';

function postProcess(response) {
  const data = response.data;
  const accBal = data.tuition_accbalance.replace(',', '');
  if (data.tuition_accbalance.match(' CR')) {
    data.tuition_accbalance = -1 * parseFloat(accBal.replace(' CR', ''));
  } else {
    data.tuition_accbalance = parseFloat(accBal);
  }
  data.pce_accbalance = parseFloat(data.pce_accbalance.replace(',', ''));
  // data.tuition_due is ignored
  return data;
};

const customActions = {
  fetch: fetchBuilder('/api/v1/finance/', postProcess, 'json'),
};

export default buildWith(
  {customActions}
);