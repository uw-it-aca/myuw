import dayjsCommon from 'dayjs';

import calendar from "dayjs/plugin/calendar";
import relativeTime from "dayjs/plugin/relativeTime";
import timezone from "dayjs/plugin/timezone";
import utc from "dayjs/plugin/utc";
import advancedFormat from "dayjs/plugin/advancedFormat";
import localizedFormat from "dayjs/plugin/localizedFormat";
import customParseFormat from "dayjs/plugin/customParseFormat";

dayjsCommon.extend(advancedFormat)
dayjsCommon.extend(calendar)
dayjsCommon.extend(relativeTime)
dayjsCommon.extend(utc)
dayjsCommon.extend(timezone)
dayjsCommon.extend(localizedFormat)
dayjsCommon.extend(customParseFormat)

dayjsCommon.tz.setDefault("America/Los_Angeles");
// default tz of dates in SDB

export const dayjs = dayjsCommon;

export const getNow = (rootState = null) => {
  if (rootState && rootState.cardDisplayDates &&
      rootState.cardDisplayDates.comparison_date) {
    return dayjs(rootState.cardDisplayDates.comparison_date);
  }
  // dayjs.tz.setDefault("America/Los_Angeles");
  // default value using client device local timezone
  return dayjs();
};

export const getTime = (dateObj) => {
  return dateObj.format('LT');
};

// Returns a - b while ignoring the date
export const diffIgnoreDate = (a, b) => {
  let diff = 0;
  diff += a.hour() - b.hour();
  diff *= 60;
  diff += a.minute() - b.minute();
  diff *= 60;
  diff += a.second() - b.second();
  diff *= 1000;
  diff += a.millisecond() - b.millisecond();
  return diff;
};

export const parseDate = (dateStr) => {
  let parsableDate = JSON.parse(JSON.stringify(dateStr));

  // Convert 2021-08-24 17:00:00+00:00 => 2021-08-24T17:00:00+00:00
  // See MUWM-4979
  if (parsableDate.match(/\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}/)) {
    parsableDate = parsableDate.substring(0, 10) + "T" + parsableDate.substring(11);
  }

  return dayjs(parsableDate);
}

export const bothellCampus = (section) => {
  return section.course_campus.toLowerCase() === 'bothell';
}

export const tacomaCampus = (section) => {
  return section.course_campus.toLowerCase() === 'tacoma';
}

export const termId = (quarter) => {
  if (quarter.toLowerCase() === "winter") return '1';
  if (quarter.toLowerCase() === "spring") return '2';
  if (quarter.toLowerCase() === "summer") return '3';
  return '4';
}
