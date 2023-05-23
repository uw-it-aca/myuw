<template>
  <div class="mx-n3 mb-2 p-3 myuw-text-sm myuw-em-links">
    Zoom now has a permanent spot in the Quick Links above.
    You can add other links by customizing your Quick Links,
    including adding recently visited links from below.
  </div>
</template>

<script>
import { mapState } from 'vuex';
export default {
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import '../../../../myuw/static/css/myuw/variables.scss';

.myuw-em-links {
  background-color: lighten(map.get($theme-colors, "beige"), 10%) !important;
}

</style>
