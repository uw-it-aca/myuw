<template>
  <div>
    <a id="og_workday" :class="extraClass" href="https://wd5.myworkday.com/uw/login.htmld" data-linklabel="Workday" :style="workdayIconStyle">{{ linkText }}</a>
  </div>
</template>

<script>
import {mapState} from 'vuex';

export default {
  props: {
    'extraClass': {
      type: String,
      default: 'myuw-workday-btn myuw-btn btn btn-default',
    },
    'linkText': {
      type: String,
      default: 'Sign in to Workday',
    },
  },
  computed: mapState({
    workdayIconStyle: (state) => 'background-image: url(\'' + state.staticUrl + 'images/wday_logo.png\';',
  }),
};
</script>

<style lang="scss" scoped>
</style>
