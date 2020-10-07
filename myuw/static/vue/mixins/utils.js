
export default {
  methods: {
    ucfirst: function (s) {
      return s.replace(/^([a-z])/, (c) => c.toUpperCase());
    },
  },
}