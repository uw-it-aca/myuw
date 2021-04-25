import dayjsCommon from 'dayjs';

dayjsCommon.extend(require('dayjs/plugin/advancedFormat'))
dayjsCommon.extend(require('dayjs/plugin/calendar'))
dayjsCommon.extend(require('dayjs/plugin/relativeTime'))
dayjsCommon.extend(require('dayjs/plugin/timezone'))
dayjsCommon.extend(require('dayjs/plugin/utc'))
dayjsCommon.extend(require('dayjs/plugin/localizedFormat'))
dayjsCommon.extend(require('dayjs/plugin/customParseFormat'))

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
  // timezone unaware format
  return dayjs.tz(dateStr, "America/Los_Angeles");
};

export const getTime = (dateObj) => {
  return dateObj.format('LT');
};
