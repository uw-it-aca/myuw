import moment, { max } from 'moment';
import {fetchBuilder, setTermAndExtractData, buildWith} from './model_builder';

const postProcess = (response, urlExtra) => {
  const schedule = setTermAndExtractData(response, urlExtra);

  schedule[urlExtra].periods = schedule[urlExtra].periods.map((period) => {
    let eosAlreadyAdded = false;
    period.eosData = [];

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
        console.log(period.sections[i].meetings[j].eos_start_date)
        // Skip if time and date are tdb or null anyways
        if (
          !period.sections[i].meetings[j].days_tbd &&
          period.sections[i].meetings[j].start_time &&
          period.sections[i].meetings[j].end_time
        ) {
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

        if (
          period.sections[i].meetings[j].eos_start_date &&
          period.sections[i].meetings[j].eos_end_date
        ) {
          period.sections[i].meetings[j].start_end_same = (
            period.sections[i].meetings[j].eos_start_date ===
            period.sections[i].meetings[j].eos_end_date
          );

          period.sections[i].meetings[j].eos_start_date = moment(
            period.sections[i].meetings[j].eos_start_date
          );
          period.sections[i].meetings[j].eos_end_date = moment(
            period.sections[i].meetings[j].eos_end_date
          );

          if (!eosAlreadyAdded) {
            period.eosData.push(period.sections[i]);
            eosAlreadyAdded = true;
          }
        }
      }

      // Some eos meetings don't come in a sorted order, so
      // we need to sort them
      if (eosAlreadyAdded) {
        period.sections[i].meetings.sort(
          (s1, s2) => {
            return s1.eos_start_date - s2.eos_start_date;
          }
        );
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