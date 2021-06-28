import dayjs from 'dayjs';
import {mapState} from 'vuex';

dayjs.extend(require('dayjs/plugin/calendar'))
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
    today: () => dayjs().hour(0).minute(0).second(0).millisecond(0),
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
    titleCaseWord(w) {
      if (w && w.length) {
        return w[0].toUpperCase() + w.substr(1).toLowerCase();
      }
      return "";
    },
    titleCaseName(nameStr) {
      return nameStr.split(' ').map(this.titleCaseWord).join(' ');
    },
    titilizeTerm(term) {
      //Takes a term string (Eg summer 2013, b-term)
      //returns a title (Eg Summer 2013 B-Term)
      let i;
      let pieces = term.split(/ |, |,/);
      let string = "";
      for (i = 0; i < pieces.length; i += 1) {
          if (i > 0) {
              string += " ";
          }
          string += this.capitalizeString(pieces[i]);
      }
      return string;
    },
    capitalizeString(string) {
      if (string === undefined) {
        return;
      }
      if (string.match(/^(full|[ab])-term$/gi)) {
          return string.split("-").map(this.titleCaseWord).join('-');
      }
      if (!string) {
          return "";
      }
      return this.titleCaseWord(string);
    },
    pageTitleFromTerm(termStr) {
      let pageTitle = termStr.split(',');
      let term = pageTitle[1];
      pageTitle[1] = pageTitle[0];
      pageTitle[0] = term;
      return pageTitle.map((s) => this.capitalizeString(s)).join(' ');
    },
    nowDatetime(useCompDate = true) {
      if (useCompDate && this.cardDisplayDates && this.cardDisplayDates.comparison_date) {
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
      return !date_str || date_str.length === 0 ? '' : dayjs(date_str).format("ddd, MMM D");
    },
    toFriendlyDatetime(date_str) {
      return !date_str || date_str.length === 0 ? '' : dayjs(date_str).format("ddd, MMM D, h:mmA");
    },
    toFromNowDate(date_str) {
      return (!date_str || date_str.length === 0 ? '' : dayjs(date_str).from(this.today()));
    },
    toCalendar(date_str) {
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
      console.log(obj);
      return Object.entries(obj).length !== 0;
    }
  },
}
