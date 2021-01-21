import dayjs from 'dayjs';
dayjs.extend(require('dayjs/plugin/timezone'))

export const getNow = (rootState) => {
  // dayjs.tz.setDefault("America/Los_Angeles");
  if (rootState && rootState.cardDisplayDates &&
      rootState.cardDisplayDates.comparison_date) {
    return dayjs(rootState.cardDisplayDates.comparison_date);
  }
  return dayjs();
}
