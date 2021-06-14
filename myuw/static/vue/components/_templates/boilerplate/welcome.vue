<template>
  <div class="p-3 myuw-welcome">
    <ul class="m-0 list-unstyled myuw-text-xs text-wrap">
      <li class="mb-1">
        <div>
          <b-button
            v-b-modal.tourModal
            variant="link"
            size="sm"
            class="p-0 m-0 text-body text-left myuw-text-xs"
          >
            See MyUW at a glance
          </b-button>
        </div>
      </li>
      <li class="mb-1">
        <b-link 
          v-out="'MyUW Help Center'"
          href="https://itconnect.uw.edu/learn/tools/myuw-help-center/#annotated"
          class="text-body"
        >
          Learn more about MyUW
        </b-link>
      </li>
    </ul>
  </div>
</template>

<script>
import {mapState} from 'vuex';

export default {
  computed: mapState({
    staticUrl: (state) => state.staticUrl,
  }),
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import "../../../../css/myuw/variables.scss";

.myuw-welcome {
  background: $gray-300;
}
</style>
