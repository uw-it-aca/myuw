<template>
    <div class="myuw-text-sm text-dark-gray fst-italic" :class="[$mq === 'mobile' ? 'text-center' : 'text-end']">
      Most updates become available after 15 minutes.

      <a
        role="button"
        class="cache-msg"
        data-bs-container="body"
        data-bs-toggle="popover"
        title="Data Update Policy"
        data-bs-placement="bottom"
        data-bs-html="true"
        :data-bs-content="message"
      >
        <font-awesome-icon :icon="faQuestionCircle" class="text-dark-gray" />
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
      return "<p>Most data updates become available in MyUW every 15 minutes, but some can take up to four hours.</p>" +
      "<div>If you’re not seeing information you’d expect, please refresh the page at " +
      "a later time. If you're still having issues email <a href='mailto:help@uw.edu?subject=MyUW Question'>" +
      "help@uw.edu</a>.</div>";
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
