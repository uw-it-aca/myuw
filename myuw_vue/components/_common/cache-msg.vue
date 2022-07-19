<template>
  <div class="myuw-text-md fst-italic text-end">
    Is something missing? Most data updates every 15 minutes.

    <a
      role="button"
      class="cache-msg"
      data-bs-container="body"
      data-bs-toggle="popover"
      data-bs-placement="bottom"
      data-bs-html="true"
      :data-bs-content="message"
    >
      <font-awesome-icon :icon="faQuestionCircle" />
    </a>
  </div>
</template>

<script>
import { faQuestionCircle } from '@fortawesome/free-solid-svg-icons';
import { Popover } from 'bootstrap';

export default {
  data() {
    return {
      faQuestionCircle,
    };
  },
  computed: {
    message () {
      return "Most data in MyUW updates every 15 minutes but can take up to four hours. " +
      "If you’re not seeing information you’d expect, refresh the page and check back at " +
      "a later time, otherwise <a href='mailto:help@uw.edu?subject=MyUW Question'>" +
      "email help@uw.edu</a>";
    }
  },
  mounted() {
    var popover = new Popover(document.querySelector('.cache-msg'));
  },
};
</script>

<style lang="scss" scoped>
@use 'sass:map';
@import '../../../myuw/static/css/myuw/variables.scss';
</style>
