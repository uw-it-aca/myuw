<template>
  <div
    class="myuw-text-sm text-dark-gray fst-italic"
    :class="[$mq === 'mobile' ? 'text-center' : 'text-end']"
  >
    Most updates become available after 15 minutes.
    <uw-pop-over selector="cache-msg" title="Data Update Policy" :content="message"/>
  </div>
</template>

<script>
import PopOver from './pop-over.vue';
export default {
  components: {
    'uw-pop-over': PopOver,
  },
  computed: {
    message() {
      return (
        '<p>Most data updates become available in MyUW every 15 minutes, but some can ' +
        'take up to four hours.</p>' +
        '<div>If you’re not seeing information you’d expect, please refresh the page at ' +
        "a later time. If you're still having issues email " +
        "<a href='mailto:help@uw.edu?subject=MyUW Question'>" +
        'help@uw.edu</a>.</div>'
      );
    },
  },
};
</script>

<style lang="scss" scoped>
@use 'sass:map';
@import '@/css/variables.scss';
</style>
