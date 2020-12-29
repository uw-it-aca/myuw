import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
dayjs.extend(relativeTime);
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
    pageTitleFromTerm(termStr) {
      let pageTitle = termStr.split(',');
      let term = pageTitle[1];
      pageTitle[1] = pageTitle[0];
      pageTitle[0] = term;
      return pageTitle.map((s) => this.ucfirst(s)).join(' ');
    },
    ucfirst(s) {
      if (s) {
        return s.replace(/^([a-z])/, (c) => c.toUpperCase());
      }
      return "";
    },
    titleCaseName(nameStr) {
      return nameStr.split(' ').map(function(w) {
        return w[0].toUpperCase() + w.substr(1).toLowerCase();
      }).join(' ');
    },
    toFriendlyDate(date_str) {
      return (!date_str || date_str.length === 0 ? '' :
              dayjs(date_str).format("ddd, MMM D"));
    },
    toFriendlyDatetime(date_str) {
      return (!date_str || date_str.length === 0 ? '' :
              dayjs(date_str).format("ddd, MMM D, h:mmA"));
    },
    toFromNowDate(date_str) {
      return (!date_str || date_str.length === 0 ? '' :
              dayjs(date_str).fromNow());
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
