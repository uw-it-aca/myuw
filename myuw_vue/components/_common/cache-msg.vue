<template>
  <div class="myuw-text-md fst-italic text-end">
    Is something missing? Most data updates every 15 minutes.
    <a data-bs-container="body" 
      data-bs-toggle="popover" 
      data-bs-placement="bottom" 
      title="hello" 
      data-bs-content="Bottom popover">
      <font-awesome-icon :icon="faQuestionCircle" />Popover on bottom
    </a>
  </div>
</template>

<script>
import {
  faQuestionCircle,
} from '@fortawesome/free-solid-svg-icons';
import {mapState} from 'vuex';
import { Popover } from 'bootstrap';

export default {
  computed: {
    ...mapState({
      pageLoadedDt: (state) => state.cardDisplayDates.comparison_date,
    }),
  },
  methods: {
  },
    data() {
    return {
      faQuestionCircle,
    }
  },
};
</script>

<style lang="scss" scoped>
@use 'sass:map';
@import '../../../myuw/static/css/myuw/variables.scss';

</style>
