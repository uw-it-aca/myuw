import dayjs from 'dayjs';
import {fetchBuilder, setTermAndExtractData, buildWith} from './model_builder';

var customParseFormat = require('dayjs/plugin/customParseFormat')
dayjs.extend(customParseFormat)

// Helper functions
const isFinalPeriod = (period) => period.id === 'finals';
const tryConvertDayJS = (obj, format=undefined) => {
  if (obj) {
    return dayjs(obj, format);
  }
  return obj;
};
const convertPeriodTimeAndDateToDateJSObj = (period) => {
  period.start_date = tryConvertDayJS(period.start_date);
  period.end_date = tryConvertDayJS(period.end_date);

  // Convert inside every section
  period.sections.forEach((section) => {
    section.start_date = tryConvertDayJS(section.start_date);
    section.end_date = tryConvertDayJS(section.end_date);

    // Convert everything in the final_exam field
    if (section.final_exam) {
      section.final_exam.start_date =
        tryConvertDayJS(section.final_exam.start_date);
      section.final_exam.end_date =
        tryConvertDayJS(section.final_exam.end_date);
    }

    // Convert inside every meeting
    section.meetings.forEach((meeting) => {
      meeting.start_time = tryConvertDayJS(meeting.start_time, "hh:mm");
      meeting.end_time = tryConvertDayJS(meeting.end_time, "hh:mm");
      meeting.eos_start_date = tryConvertDayJS(meeting.eos_start_date);
      meeting.eos_end_date = tryConvertDayJS(meeting.eos_end_date);
    });
  });
};
const convertTermTimeAndDateToDateJSObj = (term) => {
  term.aterm_last_date = tryConvertDayJS(term.aterm_last_date);
  term.bterm_first_date = tryConvertDayJS(term.bterm_first_date);
  term.first_day_quarter = tryConvertDayJS(term.first_day_quarter);
  term.end_date = tryConvertDayJS(term.end_date);
  term.last_day_instruction = tryConvertDayJS(term.last_day_instruction);
  term.last_final_exam_date = tryConvertDayJS(term.last_final_exam_date);
};

const postProcess = (response, urlExtra) => {
  const schedule = setTermAndExtractData(response, urlExtra);

  convertTermTimeAndDateToDateJSObj(schedule[urlExtra].term);
  schedule[urlExtra].periods.forEach((period) => {
    // Do conversions to dayjs objects from time and date
    convertPeriodTimeAndDateToDateJSObj(period);
    period.eosData = [];

    if (period.end_date && period.start_date) {
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
      let eosAlreadyAdded = false;
      // Skip if no exam is defined or no time is set
      if (section.final_exam && section.final_exam.start_date) {
        if (isFinalPeriod(period)) {
          // Generate time relative to today so that it can be compared
          let startTime = dayjs()
            .hour(section.final_exam.start_date.hour())
            .minute(section.final_exam.start_date.minute())
            .second(0);
          let endTime = dayjs()
            .hour(section.final_exam.end_date.hour())
            .minute(section.final_exam.end_date.minute())
            .second(0);

          // Update min and max time if needed
          if (earliestTime === null && latestTime === null) {
            earliestTime = startTime;
            latestTime = endTime;
          } else {
            if (startTime < earliestTime) {
              earliestTime = startTime;
            }
            if (endTime > latestTime) {
              latestTime = endTime;
            }
          }
        }
      }

      section.meetings.forEach((meeting) => {
        // Skip if time and date are tdb or null anyways
        if (
          !meeting.days_tbd &&
          !meeting.no_meeting &&
          meeting.start_time &&
          meeting.end_time
        ) {
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
            meeting.eos_start_date.format() === meeting.eos_end_date.format()
          );
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

    // Generate Days
    period.daySlots = {};
    if (!isFinalPeriod(period)) {
      if (period.meets_sunday) {
        period.daySlots['sunday'] = null;
      }
      period.daySlots['monday'] = null;
      period.daySlots['tuesday'] = null;
      period.daySlots['wednesday'] = null;
      period.daySlots['thursday'] = null;
      period.daySlots['friday'] = null;
      if (period.meets_saturday) {
        period.daySlots['saturday'] = null;
      }
    } else if (earliestTime) {
      // Generate dates if on a final period

      let refrenceDate = earliestTime;

      if (refrenceDate.day() === 6) {
        period.daySlots['saturday'] = refrenceDate.clone();
        period.daySlots['monday'] = refrenceDate.clone().day(8);
        period.daySlots['tuesday'] = refrenceDate.clone().day(9);
        period.daySlots['wednesday'] = refrenceDate.clone().day(10);
        period.daySlots['thursday'] = refrenceDate.clone().day(11);
        period.daySlots['friday'] = refrenceDate.clone().day(12);
      } else if (refrenceDate.day() > 0) {
        period.daySlots['monday'] = refrenceDate.clone().day(1);
        period.daySlots['tuesday'] = refrenceDate.clone().day(2);
        period.daySlots['wednesday'] = refrenceDate.clone().day(3);
        period.daySlots['thursday'] = refrenceDate.clone().day(4);
        period.daySlots['friday'] = refrenceDate.clone().day(5);
      }
    } else {
      period.daySlots = {
        monday: null,
        tuesday: null,
        wednesday: null,
        thursday: null,
        friday: null
      };
    }

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