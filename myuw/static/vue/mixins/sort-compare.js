export default {
  methods: {
    isUndefinedOrNull(value) {
      return value === undefined || value === null;
    },

    normalizeValue(value) {
      // `null` / `undefined` => ''
      // `'0'` => `0`
      if (this.isUndefinedOrNull(value)) {
        return '';
      }
      const RX_NUMBER = /^[0-9][,.0-9]+$/
      if (typeof value === 'string' && RX_NUMBER.test(value)) {
        return parseFloat(value.replace(',', ''));
      }
      return value;
    },

    defaultSortCompare(a, b, {sortByField = null, nullLast = false} = {}) {
      let aa = sortByField ? a[sortByField] : a;
      let bb = sortByField ? b[sortByField] : b;

      if (nullLast) {
        // Special case when sorting `null` / `undefined` last
        if (this.isUndefinedOrNull(aa) && !this.isUndefinedOrNull(bb)) {
          return 1;
        }
        if (!this.isUndefinedOrNull(aa) && this.isUndefinedOrNull(bb)) {
          return -1;
        }
      }
      aa = this.normalizeValue(aa);
      bb = this.normalizeValue(bb);
      return aa < bb ? -1 : aa > bb ? 1 : 0;
    },
  }
}
