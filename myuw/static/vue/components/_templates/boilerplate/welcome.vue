<template>
  <div class="p-3 bg-light-gray">
    <ul class="m-0 list-unstyled myuw-text-xs text-wrap">
      <li class="mb-1">
        <div>
          <button v-b-modal.tourModal
            type="button"
            class="btn btn-link btn-sm p-0 m-0 text-body text-left myuw-text-xs"
          >
            See MyUW at a glance
          </button>
        </div>
      </li>
      <li class="mb-1">
        <a
          v-out="'MyUW Help Center'"
          href="https://itconnect.uw.edu/learn/tools/myuw-help-center/#annotated"
          class="text-body"
        >
          Learn more about MyUW
        </a>
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
</style>
