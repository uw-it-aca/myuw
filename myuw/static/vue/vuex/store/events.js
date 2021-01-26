import {fetchBuilder, buildWith} from './model_builder';
import {
  strToDate,
} from './common';

const postProcess = (response) => {
  const eventData = response.data;
  let futureCalCount = 0;

  // Set it to itself if it is defined otherwise set it
  // to a empty array.
  eventData.future_active_cals = eventData.future_active_cals || [];
  eventData.events = eventData.events || [];

  eventData.future_active_cals.forEach((event) => {
    futureCalCount += event.count;
  });

  eventData.events.forEach((event) => {
    event.start_date = strToDate(event.start);
    event.start_time = event.start_date.format('h:mm A');
    event.end_date = strToDate(event.end);
  });

  return {
    shownEvents: eventData.events.slice(0, 6),
    hiddenEvents: eventData.events.slice(6),
    futureCalCount: futureCalCount,
    futureCalLinks: eventData.future_active_cals,
    calLinks: eventData.active_cals,
  };
}

const customActions = {
    fetch: fetchBuilder('/api/v1/deptcal/', postProcess, 'json'),
};

export default buildWith(
    {customActions},
);
