<template>
  <b-card
    v-if="loaded"
    class="rounded-0 shadow-sm mb-3"
  >
    <slot name="card-heading" />
    <slot name="card-body" />
  </b-card>
  <b-card
    v-else
    class="rounded-0 shadow-sm mb-3"
  >
    <b-card-text class="d-flex justify-content-center card-loading">
      <!-- TODO: replace this with a cog -->
      <b-spinner
        small
        variant="muted"
        class="my-auto"
        label="Loading..."
      />
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
  },
  data: function() {
    return {};
  },
};
</script>

<style lang="scss">
@import '../../css/myuw-variables.scss';

.myuw-card-header {
  color: $uw-gold
}

</style>
