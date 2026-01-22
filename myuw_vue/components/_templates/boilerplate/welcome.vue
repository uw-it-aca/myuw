<template>
  <div class="p-3 bg-light-gray">
    <ul class="m-0 list-unstyled text-wrap">
      <li class="mb-1">
        <div>
          <button v-uw-modal.tourModal
            type="button"
            class="btn btn-link btn-sm p-0 m-0 text-body text-start"
          >
            See MyUW at a glance
          </button>
        </div>
      </li>
      <li class="mb-1">
        <a
          v-out="'MyUW Help Center'"
          href="https://uwconnect.uw.edu/it?id=kb_article_view&sysparm_article=KB0033852"
          class="text-body small"
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
