<template>
  <div class="myuw-text-md fst-italic text-end">
    Is something missing? Most data updates every 15 minutes.

    <a
      class="test-popover"
      data-bs-container="body"
      data-bs-toggle="popover"
      data-bs-placement="bottom"
      title="hello"
      data-bs-content="Bottom popover"
    >
      <font-awesome-icon :icon="faQuestionCircle" />
    </a>
  </div>
</template>

<script>
import { faQuestionCircle } from '@fortawesome/free-solid-svg-icons';
import { mapState } from 'vuex';
import { Popover } from 'bootstrap';

export default {
  data() {
    return {
      faQuestionCircle,
    };
  },
  computed: {
    ...mapState({
      pageLoadedDt: (state) => state.cardDisplayDates.comparison_date,
    }),
  },
  mounted() {
    var popover = new Popover(document.querySelector('.test-popover'));
  },
  methods: {},

};
</script>

<style lang="scss" scoped>
@use 'sass:map';
@import '../../../myuw/static/css/myuw/variables.scss';
</style>
