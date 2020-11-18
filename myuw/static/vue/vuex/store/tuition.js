import {fetchBuilder, extractData, buildWith} from './model_builder';
import dayjs from 'dayjs';

const postProcess = (response) => {
  const data = response.data;
  if (data.tuition_accbalance.match(' CR')) {
    data.tuition_accbalance = -1 * parseFloat(data.tuition_accbalance.replace(' CR', ''));
  } else {
    data.tuition_accbalance = parseFloat(data.tuition_accbalance);
  }
  data.pce_accbalance = parseFloat(data.pce_accbalance);
  if (data.tuition_accbalance > 0) {
    let tuition_due = dayjs(data.tuition_due, 'YYYY-MM-DD');
    let diff = Math.ceil(tuition_due.diff(dayjs(), 'day', true));
    if (diff === 0) {
      data.due_today = true;
    } else if (diff === 1) {
      data.due_tomorrow = true;
    } else if (diff < 0) {
      data.past_due = true;
    }
  }

  return data;
};

const customActions = {
  fetch: fetchBuilder('/api/v1/finance/', postProcess, 'json'),
};

export default buildWith(
  {customActions}
);