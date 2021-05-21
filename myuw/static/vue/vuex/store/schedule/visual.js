import {fetchBuilder, setTermAndExtractData, buildWith} from '../model_builder';
import {
  tryConvertDayJS,
  processSectionDates,
  processSectionMeetings,
  convertTermTimeAndDateToDateJSObj,
  generateMeetingLocationData,
} from './common';
import {dayjs} from '../common';

var customParseFormat = require('dayjs/plugin/customParseFormat')
dayjs.extend(customParseFormat)

// Helper functions
const isFinalPeriod = (period) => period.id === 'finals';

const convertPeriodTimeAndDateToDateJSObj = (period) => {
  period.start_date = tryConvertDayJS(period.start_date);
  period.end_date = tryConvertDayJS(period.end_date);
  period.sections.forEach((section) => {
    // Convert inside every section
    processSectionDates(section);
    processSectionMeetings(section);
  });
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
    let finalPeriod = isFinalPeriod(period);
    period.sections.forEach((section) => {
      let eosAlreadyAdded = false;
      // Skip if no exam is defined or no time is set
      if (section.final_exam && section.final_exam.start_date) {
        section.final_exam.locationData =
          generateMeetingLocationData(section.final_exam);
        if (finalPeriod) {
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
        if (
          !meeting.days_tbd &&
          !meeting.no_meeting &&
          meeting.start_time &&
          meeting.end_time
        ) {
          if (!finalPeriod) {
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

        meeting.locationData = generateMeetingLocationData(meeting);
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
    if (!finalPeriod) {
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

  let firstPeriod = schedule?.[urlExtra]?.periods?.[0];
  if (firstPeriod && firstPeriod.id === 'finals') {
    schedule[urlExtra].noPeriodsNoMeetings = firstPeriod.earliestMeetingTime === null &&
      firstPeriod.latestMeetingTime === null;
  }

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