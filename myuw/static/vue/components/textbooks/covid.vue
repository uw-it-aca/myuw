<template>
  <div>
    <b-alert show variant="dark-beige" class="myuw-textbook-covid">
      <div class="d-flex text-dark-beige m-0 myuw-text-md">
        <div class="pr-2 flex-shrink-1">
          <font-awesome-icon :icon="faExclamationTriangle" />
        </div>
        <div class="w-100 font-weight-bold">
          University Book Store Autumn 2020 Update
        </div>
      </div>
      <hr>
      <div class="text-dark-beige myuw-text-md">
        In order to ensure public health, all course materials purchases for
        Fall 2020 quarter are online only; University Book Store&rsquo;s
        course materials department will be closed to the public.
      </div>
    </b-alert>
  </div>
</template>

<script>
import {
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';

export default {
  data() {
    return {
      faExclamationTriangle,
    };
  },
}
</script>

<style lang="scss" scoped>
@use "sass:map";
@import "../../../css/myuw/variables.scss";
.myuw-textbook-covid {
  background: lighten(map.get($theme-colors, "warning"), 48%) !important;
}
</style>
