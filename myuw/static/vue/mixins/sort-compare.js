export default {
  methods: {
    normalizeValue(value) {
      if (value === undefined || value === null) {
        return '';
      }
      if (toType(value) === 'number') {
        return parseFloat(value.replace(',', ''));
      }
      return value;
    },

    defaultSortCompare(a, b, {sortByField = null, nullLast = false} = {}) {
      let aa = sortByField ? a[sortByField] : a;
      let bb = sortByField ? b[sortByField] : b;

      // Internally normalize value
      // `null` / `undefined` => ''
      // `'0'` => `0`
      aa = normalizeValue(aa);
      bb = normalizeValue(bb);

      if (isNumber(aa) && isNumber(bb)) {
        return aa < bb ? -1 : aa > bb ? 1 : 0;
      } else if (nullLast && aa === '' && bb !== '') {
        // Special case when sorting `null` / `undefined` / '' last
        return 1;
      } else if (nullLast && aa !== '' && bb === '') {
        // Special case when sorting `null` / `undefined` / '' last
        return -1;
      } else {
        return aa - bb;
      }
    },
  }
}
