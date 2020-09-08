import moment, { max } from 'moment';
import {fetchBuilder, setTermAndExtractData, buildWith} from './model_builder';

// Helper functions
const isFinalPeriod = (period) => period.id === 'finals';

const postProcess = (response, urlExtra) => {
  const schedule = setTermAndExtractData(response, urlExtra);

  schedule[urlExtra].periods.forEach((period) => {
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
    period.sections.forEach((section) => {
      // Skip if no exam is defined or no time is set
      if (section.final_exam && section.final_exam.start_date) {
        section.final_exam.start_date = moment(
          section.final_exam.start_date
        ).seconds(0).milliseconds(0);
        section.final_exam.end_date = moment(
          section.final_exam.end_date
        ).seconds(0).milliseconds(0);

        if (isFinalPeriod(period)) {
          // Update min and max time if needed
          if (earliestTime === null && latestTime === null) {
            earliestTime = section.final_exam.start_date;
            latestTime = section.final_exam.end_date;
          } else {
            if (section.final_exam.start_date < earliestTime) {
              earliestTime = section.final_exam.start_date;
            }
            if (section.final_exam.end_date > latestTime) {
              latestTime = section.final_exam.end_date;
            }
          }
        }
      }

      section.meetings.forEach((meeting) => {
        // Skip if time and date are tdb or null anyways
        if (!meeting.days_tbd && meeting.start_time && meeting.end_time) {
          meeting.start_time = moment(
            meeting.start_time, "hh:mm"
          ).seconds(0).milliseconds(0);
          meeting.end_time = moment(
            meeting.end_time, "hh:mm"
          ).seconds(0).milliseconds(0);

          if (!isFinalPeriod(period)) {
            // Update min and max time if needed
            if (earliestTime === null && latestTime === null) {
              earliestTime = meeting.start_time;
              latestTime = meeting.end_time;
            } else {
              if (meeting.start_time < earliestTime) {
                earliestTime = meeting.start_time;
              }
              if (meeting.end_time > latestTime) {
                latestTime = meeting.end_time;
              }
            }
          }
        }

        if (meeting.eos_start_date && meeting.eos_end_date) {
          meeting.start_end_same = (
            meeting.eos_start_date === meeting.eos_end_date
          );

          meeting.eos_start_date = moment(meeting.eos_start_date);
          meeting.eos_end_date = moment(meeting.eos_end_date);
        }

        if (section.eos_cid && !eosAlreadyAdded) {
          period.eosData.push(section);
          eosAlreadyAdded = true;
        }
      });

      // Some eos meetings don't come in a sorted order, so
      // we need to sort them
      if (eosAlreadyAdded) {
        section.meetings.sort(
          (s1, s2) => s1.eos_start_date - s2.eos_start_date
        );
      }
    });

    period.earliestMeetingTime = earliestTime ? earliestTime.clone() : null;
    period.latestMeetingTime = latestTime ? latestTime.clone() : null;
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