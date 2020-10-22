<template>
  <div class="p-3 myuw-welcome">
    <p class="mb-1 text-dark myuw-text-md">
      Welcome!
    </p>
    <ul class="m-0 list-unstyled myuw-text-xs">
      <li>
        <b-button v-b-modal.tourModal variant="link" size="sm"
                  class="p-0 m-0 text-muted myuw-text-xs"
                  aria-hidden="true"
        >
          See MyUW at a glance
        </b-button>
      </li>
      <li>
        <b-link
          :href="learnMoreURL"
          class="text-muted"
          target="_blank"
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
  data: function() {
    return {
      learnMoreURL:
        '/out?u=https%3A%2F%2Fitconnect.uw.edu%2Flearn%2Ftools%2Fmyuw-help-center%2F%23annotated&amp;l=MyUW%20Help%20Center',
    };
  },
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
