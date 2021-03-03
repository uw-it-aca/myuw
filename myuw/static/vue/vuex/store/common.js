import dayjs from 'dayjs';

dayjs.extend(require('dayjs/plugin/advancedFormat'))
dayjs.extend(require('dayjs/plugin/calendar'))
dayjs.extend(require('dayjs/plugin/relativeTime'))
dayjs.extend(require('dayjs/plugin/timezone'))
dayjs.extend(require('dayjs/plugin/utc'))

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
  return dayjs.tz(dateStr, "America/Los_Angeles");
};

