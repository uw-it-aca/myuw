import moment from 'moment-timezone';
import { buildWith } from './model_builder';

const postProcess = (response) => {
  const eventData = response.data;
  const futureCalCount = 0;

  for (const [_key, event] of Object.entries(eventData.future_active_cals)) {
    futureCalCount += event.count;
  }

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
    needsDisclosure: eventData.events.length > 6,
    futureCalCount: futureCalCount,
    futureCalLinks: eventData.future_active_cals,
    calLinks: eventData.active_cals,
  };
}

export default buildWith(
  '/api/v1/deptcal/',
  postProcess,
);
