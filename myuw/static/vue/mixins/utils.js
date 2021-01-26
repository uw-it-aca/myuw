import dayjs from 'dayjs';
dayjs.extend(require('dayjs/plugin/calendar'))
dayjs.extend(require('dayjs/plugin/relativeTime'))
dayjs.extend(require('dayjs/plugin/timezone'))
dayjs.extend(require('dayjs/plugin/utc'))

export default {
  methods: {
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
    ucfirst(s) {
      if (s && s.length) {
        return s.replace(/^([a-z])/, (c) => c.toUpperCase());
      }
      return "";
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
    nowDatetime(cardDisplayDates = null) {
      if (cardDisplayDates && cardDisplayDates.comparison_date) {
        return dayjs(cardDisplayDates.comparison_date);
      }
      // dayjs.tz.setDefault("America/Los_Angeles");
      // using client device's timezone
      return dayjs();
    },
    strToDayjs(dateStr) {
      // convert date or datetime string to dayjs
      return dayjs.tz(dateStr, "America/Los_Angeles");
    },
    toFriendlyDate(date_str) {
      return !date_str || date_str.length === 0 ? '' : dayjs(date_str).format("ddd, MMM D");
    },
    toFriendlyDatetime(date_str) {
      return !date_str || date_str.length === 0 ? '' : dayjs(date_str).format("ddd, MMM D, h:mmA");
    },
    toFromNowDate(date_str) {
      return (!date_str || date_str.length === 0 ? '' : dayjs(date_str).fromNow());
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
  },
}
