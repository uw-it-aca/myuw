import dayjs from 'dayjs';
import {mapState} from 'vuex';

dayjs.extend(require('dayjs/plugin/calendar'))
dayjs.extend(require('dayjs/plugin/duration'))
dayjs.extend(require('dayjs/plugin/relativeTime'))
dayjs.extend(require('dayjs/plugin/timezone'))
dayjs.extend(require('dayjs/plugin/utc'))
dayjs.extend(require('dayjs/plugin/isToday'));
dayjs.extend(require('dayjs/plugin/weekOfYear'));
dayjs.extend(require('dayjs/plugin/advancedFormat'))
dayjs.extend(require('dayjs/plugin/localizedFormat'))
dayjs.extend(require('dayjs/plugin/customParseFormat'))

// default tz of dates in SDB
dayjs.tz.setDefault("America/Los_Angeles");

export default {
  computed: {
    ...mapState({
      cardDisplayDates: (state) => state.cardDisplayDates,
    }),
  },
  methods: {
    dayjs: dayjs,
    today: () => dayjs().hour(0).minute(0).second(0).millisecond(0),  // bof
    encodeForMaps(s) {
      if (s) {
        s = s.replace(/ \(/g, " - ");
        s = s.replace(/[\)&]/g, "");
        s = encodeURIComponent(s);
      }
      return s;
    },
    // Phone Number Utils
    parsePhoneNumber(phNumStr) {
      let parsed = null;
      if (phNumStr) {
        let matches = phNumStr.match(/^(\+(?<country>\d+) )?(?<area>\d{3})[ -\.]?(?<exchange>\d{3})[ -\.]?(?<line>\d{4})$/);
        if (matches) {
          parsed = matches.groups;
        }
      }
      return parsed;
    },
    formatPhoneNumberDisaply(phNumStr) {
      let parsed = this.parsePhoneNumber(phNumStr);
      if (parsed) {
        return `(${parsed.area}) ${parsed.exchange}-${parsed.line}`;
      }
      return "";
    },
    formatPhoneNumberLink(phNumStr) {
      let parsed = this.parsePhoneNumber(phNumStr);
      if (parsed) {
        if (parsed.country == undefined) parsed.country = "1";
        return `+${parsed.country}-${parsed.area}-${parsed.exchange}-${parsed.line}`;
      }
      return "";
    },
    sortNotices(notices) {
      return notices.sort((n1, n2) => {
        if (n1.is_critical !== n2.is_critical) {
          return n2.is_critical - n1.is_critical;
          // put critical notices before non-critical
        }
        // put notices with date before those without dates
        if (n1.sortDate !== null && n2.sortDate === null) { return -1;}
        if (n1.sortDate === null && n2.sortDate !== null) { return 1;}
        // sort in ascending order
        return n1.sortDate - n2.sortDate;
      });
    },
    degreeListString(degrees) {
      let list = '';
      for (let i = 0; i < degrees.length; i++) {
        list += degrees[i].full_name;
        if (i < degrees.length - 1) {
          list += ', ';
        }
      }
      return list;
    },
    isPreMajor(majorName) {
      return Boolean(
        majorName.match(/^EXTENDED PRE/) ||
        majorName.match(/^EXTND PRE/) ||
        majorName.match(/^PRE /) ||
        majorName.match(/^PRE-/) ||
        majorName.match(/^PREMAJOR/)
      );
    },
    noDeclaredMajor(termMajors) {
      if (termMajors) {
        const majors = termMajors[termMajors.length - 1].majors;
        for (let j = 0; j < majors.length; j++) {
          const majorName = majors[j].name;
          if (!this.isPreMajor(majorName)) {
            return false;
          }
        }
      }
      return true;
    },
    titleCaseWord(w) {
      if (w && w.length) {
        return w[0].toUpperCase() + w.substr(1).toLowerCase();
      }
      return "";
    },
    titleCaseName(nameStr) {
      return ((nameStr && nameStr.length)
        ? nameStr.split(" ").map(this.titleCaseWord).join(' ')  : "");
    },
    capitalizeString(string) {
      if (!string) {
          return "";
      }
      if (string.match(/^(full|[ab])-term$/gi)) {
          return string.split("-").map(this.titleCaseWord).join('-');
      }
      return this.titleCaseWord(string);
    },
    pageTitleFromTerm(termStr) {
      if (!termStr) {
        return "";
      }
      let pageTitle = termStr.split(',');
      let term = pageTitle[1];
      pageTitle[1] = pageTitle[0];
      pageTitle[0] = term;
      return pageTitle.map((s) => this.capitalizeString(s)).join(' ');
    },

    hasPassed(dateStr, useCompDate = true) {
      if (!dateStr) return false;

      dayjs.tz.setDefault("America/Los_Angeles");
      const dt = dayjs(dateStr);

      if (useCompDate && this.cardDisplayDates?.comparison_date) {
        return dayjs(this.cardDisplayDates.comparison_date).isAfter(dt);
      }

      return dayjs().isAfter(dt);
    },

    nowDatetime(useCompDate = true) {
      if (useCompDate && this.cardDisplayDates?.comparison_date) {
        return dayjs(this.cardDisplayDates.comparison_date);
      }
      // dayjs.tz.setDefault("America/Los_Angeles");
      // using client device's timezone
      return dayjs();
    },
    formatMeetingTime(timeStr) {
      const tObj = dayjs(timeStr, "hh:mm").second(0).millisecond(0);
      return tObj.format('h:mm A') ;
    },
    toFriendlyDate(date_str) {
      if (!date_str || date_str.length === 0) return '';
      date_str = date_str.replace(' ', 'T');  // MUWM-5095: 'T' time works on all browsers
      return dayjs(date_str).format("ddd, MMM D");
    },
    toFriendlyDatetime(date_str) {
      if (!date_str || date_str.length === 0) return '';
      date_str = date_str.replace(' ', 'T');  // MUWM-5095 'T' time works on all browsers
      return dayjs(date_str).format("ddd, MMM D, h:mmA");
    },
    toFromNowDate(date_str, useCompDate = true) {
      if (!date_str || date_str.length === 0) return '';
      // MUWM-3947
      const delta = this.timeDeltaFrom(date_str);
      if (delta < -1) return Math.abs(delta) + ' days ago';
      if (delta >= -1 && delta < 0) return "a day ago";
      if (delta >= 0 && delta < 1) return "Today";
      if (delta >= 1 && delta < 2) return "Tomorrow";
      return 'in ' + (delta - 1) + ' days';
    },
    timeDeltaFrom(date_str, unit = 'day', useCompDate = true) {
      // return the number of units that the date_str (must be a valid date/datetime string)
      // is to the comparison date.
      // https://day.js.org/docs/en/display/difference
      date_str = date_str.replace(' ', 'T');  // MUWM-5095: 'T' time works on all browsers
      return Math.ceil(dayjs(date_str).diff(this.nowDatetime(useCompDate), unit, true));
    },
    toCalendar(date_str) {
      // to be removed
      return (!date_str || date_str.length === 0 ? '' : dayjs(date_str).calendar());
    },
    formatPrice(price) {
      let formatted = price.toString().split(".");
      if (formatted[1] && formatted[1].length === 1) {
        formatted[1] += "0";
      }
      if (!formatted[1] || formatted[1].length === 0) {
        formatted[1] = "00";
      }
      return formatted.join(".");
    },
    formatDateRange(d1, d2) {
      if (d1 && d2) {
        if (d1.isSame(d2, 'day')) {
          return `${d1.format("MMM D")}`;
        } else if (d1.isSame(d2, 'month')) {
          return `${d1.format("MMM D")} - ${d2.format("D")}`;
        } else {
          return `${d1.format("MMM D")} - ${d2.format("MMM D")}`;
        }
      } else if (d1 || d2) {
        let d = d1 ? d1 : d2;
        return `${d.format("MMM D")}`;
      }
    },
    hasAnyKeys(obj) {
      return Object.entries(obj).length > 0;
    },
    classesToClassDict(classes) {
      // converts a html class attribute string to a dictionary
      let classDict = {};
      if (classes instanceof String || typeof(classes) === 'string') {
        classes.split(/\s+/).forEach((c) => classDict[c] = true);
      } else if (classes instanceof Array) {
        classes.forEach((c) => classDict[c] = true);
      } else if (classes) {
        // Want to copy here?
        Object.entries(classes).forEach(([key, value]) => classDict[key] = value);
      }
      return classDict;
    }
  },
}
