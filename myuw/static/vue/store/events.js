import moment from 'moment-timezone';
import { buildWith } from './model_builder';

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
    const startDate = moment(new Date(event.start)).tz('America/Los_Angeles');
    const endDate = moment(new Date(event.end)).tz('America/Los_Angeles');

    event.start_time = startDate.format('h:mm A');
    event.start_date = startDate;
    event.end_date = endDate;
  });

  return {
    shownEvents: eventData.events.slice(0, 6),
    hiddenEvents: eventData.events.slice(6),
    futureCalCount: futureCalCount,
    futureCalLinks: eventData.future_active_cals,
    calLinks: eventData.active_cals,
  };
}

export default buildWith(
  '/api/v1/deptcal/',
  postProcess,
);
