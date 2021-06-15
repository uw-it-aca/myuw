import dayjsCommon from 'dayjs';

dayjsCommon.extend(require('dayjs/plugin/advancedFormat'))
dayjsCommon.extend(require('dayjs/plugin/calendar'))
dayjsCommon.extend(require('dayjs/plugin/relativeTime'))
dayjsCommon.extend(require('dayjs/plugin/timezone'))
dayjsCommon.extend(require('dayjs/plugin/utc'))
dayjsCommon.extend(require('dayjs/plugin/localizedFormat'))
dayjsCommon.extend(require('dayjs/plugin/customParseFormat'))

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

export const strToDate = (dateStr) => {
  // timezone unaware date or datetime string
  return dayjs.tz(dateStr, "America/Los_Angeles");
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
  console.log(a, b, diff);
  return diff;
};
