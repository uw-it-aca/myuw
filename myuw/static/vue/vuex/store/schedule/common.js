import dayjs from 'dayjs';
import customParseFormat from 'dayjs/plugin/customParseFormat';
dayjs.extend(customParseFormat)
dayjs.extend(require('dayjs/plugin/timezone'))

export const tryConvertDayJS = (obj, format=undefined) => {
  if (obj) {
    return dayjs(obj, format).second(0).millisecond(0);
  }
  return obj;
};

export const convertTermTimeAndDateToDateJSObj = (term) => {
  if (term) {
    term.aterm_last_date = tryConvertDayJS(term.aterm_last_date);
    term.bterm_first_date = tryConvertDayJS(term.bterm_first_date);
    term.first_day_quarter = tryConvertDayJS(term.first_day_quarter);
    term.end_date = tryConvertDayJS(term.end_date);
    term.last_day_instruction = tryConvertDayJS(term.last_day_instruction);
    term.last_final_exam_date = tryConvertDayJS(term.last_final_exam_date);
  }
};

export const convertSectionsTimeAndDateToDateJSObj = (sections) => {
  sections.forEach((section) => {
    section.hasEosDates = false;
    section.showMtgType = false;
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
      section.hasEosDates = section.hasEosDates ||
        meeting.eos_start_date && meeting.eos_end_date;
      meeting.eos_start_date = tryConvertDayJS(meeting.eos_start_date);
      meeting.eos_end_date = tryConvertDayJS(meeting.eos_end_date);

      meeting.displayType = (meeting.type && meeting.type !== 'NON' &&
          meeting.type.toLowerCase() !== section.section_type.toLowerCase());
      section.showMtgType = section.showMtgType || meeting.displayType;
    });
  });
}

function encodeForMaps(s) {
  if (s) {
    s = s.replace(/ \(/g, " - ");
    s = s.replace(/[\)&]/g, "");
    s = encodeURIComponent(s);
  }
  return s;
}

export const getNow = (rootState) => {
  // dayjs.tz.setDefault("America/Los_Angeles");
  if (rootState && rootState.cardDisplayDates &&
      rootState.cardDisplayDates.comparison_date) {
    return dayjs(rootState.cardDisplayDates.comparison_date);
  }
  return dayjs();
}
