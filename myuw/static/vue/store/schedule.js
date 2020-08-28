import moment, { max } from 'moment';
import {fetchBuilder, setTermAndExtractData, buildWith} from './model_builder';

const postProcess = (response, urlExtra) => {
  const schedule = setTermAndExtractData(response, urlExtra);

  schedule[urlExtra].periods = schedule[urlExtra].periods.map((period) => {
    if (period.end_date && period.start_date) {
      // Convert dates into moment objects
      period.end_date = moment(period.end_date);
      period.start_date = moment(period.start_date);

      // Construct the title
      period.title = period.start_date.format("MMM DD") +
                     ' - ' + period.end_date.format("MMM DD");
    } else {
      // Construct the title
      period.title = period.id;
    }

    let earliestTime = null;
    let latestTime = null;
    for (const i in period.sections) {
      // Skip if no exam is defined or no time is set
      if (period.sections[i].final_exam &&
          period.sections[i].final_exam.start_date) {
        period.sections[i].final_exam.start_date = moment(
          period.sections[i].final_exam.start_date
        ).seconds(0).milliseconds(0);
        period.sections[i].final_exam.end_date = moment(
          period.sections[i].final_exam.end_date,
        ).seconds(0).milliseconds(0);

        if (period.id == 'finals') {
          // Update min and max time if needed
          if (earliestTime === null && latestTime === null) {
            earliestTime = period.sections[i].final_exam.start_date;
            latestTime = period.sections[i].final_exam.end_date;
          } else {
            if (period.sections[i].final_exam.start_date < earliestTime) {
              earliestTime = period.sections[i].final_exam.start_date;
            }
            if (period.sections[i].final_exam.end_date > latestTime) {
              latestTime = period.sections[i].final_exam.end_date;
            }
          }
        }
      }

      for (const j in period.sections[i].meetings) {
        // Skip if time and date are tdb
        if (!period.sections[i].meetings[j].days_tbd) {
          period.sections[i].meetings[j].start_time = moment(
            period.sections[i].meetings[j].start_time,
            "hh:mm"
          ).seconds(0).milliseconds(0);
          period.sections[i].meetings[j].end_time = moment(
            period.sections[i].meetings[j].end_time,
            "hh:mm"
          ).seconds(0).milliseconds(0);

          if (period.id != 'finals') {
            // Update min and max time if needed
            if (earliestTime === null && latestTime === null) {
              earliestTime = period.sections[i].meetings[j].start_time;
              latestTime = period.sections[i].meetings[j].end_time;
            } else {
              if (period.sections[i].meetings[j].start_time < earliestTime) {
                earliestTime = period.sections[i].meetings[j].start_time;
              }
              if (period.sections[i].meetings[j].end_time > latestTime) {
                latestTime = period.sections[i].meetings[j].end_time;
              }
            }
          }
        }
      }
    }

    period.earliestMeetingTime = earliestTime ? earliestTime.clone() : null;
    period.latestMeetingTime = latestTime ? latestTime.clone() : null;
    return period;
  });

  return schedule;
}

const customActions = {
  fetch: fetchBuilder(
    '/api/v1/visual_schedule/',
    postProcess,
    'json'
  ),
};

export default buildWith(
  { customActions },
);