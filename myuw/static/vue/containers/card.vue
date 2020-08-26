<template>
  <b-card v-if="loaded" class="rounded-0 shadow-sm mb-3" tabindex="0">
    <slot name="card-heading" />
    <slot name="card-body" />
    <slot name="card-disclosure" />
    <template v-if="!!this.$slots['card-footer']"
              v-slot:footer
              footer-tag="footer"
    >
      <slot name="card-footer" />
    </template>
  </b-card>
  <b-card v-else-if="errored" class="rounded-0 shadow-sm mb-3" tabindex="0">
    <slot name="card-heading" />
    <p>
      <font-awesome-icon :icon="['fas', 'exclamation-triangle']" />
      An error occurred and MyUW cannot load event information right now.
      Please try again later.
    </p>
  </b-card>
  <b-card v-else class="rounded-0 shadow-sm mb-3">
    <b-card-text class="d-flex justify-content-center card-loading">
      <!-- TODO: replace this with a cog -->
      <b-spinner small variant="muted" class="my-auto" label="Loading..." />
    </b-card-text>
  </b-card>
</template>

<script>
export default {
  props: {
    loaded: {
      type: Boolean,
      default: false,
    },
    errored: {
      type: Boolean,
      default: false,
    },
  },
  data: function() {
    return {};
  },
};
</script>

<style lang="scss">
@import "../../css/myuw-variables.scss";

.myuw-card-header {
  color: $uw-gold;
}
</style>
