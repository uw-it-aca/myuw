<template>
  <div class="myuw-text-md fst-italic text-end">
    This page was last loaded at 9:26 AM. Is something missing?
  </div>
</template>

<script>
import {mapState} from 'vuex';

export default {
  computed: {
    ...mapState({
      pageLoadedDt: (state) => state.cardDisplayDates.comparison_date,
    }),
  },
  methods: {
  },
};
</script>

<style lang="scss" scoped>
@use 'sass:map';
@import '../../../myuw/static/css/myuw/variables.scss';

</style>
