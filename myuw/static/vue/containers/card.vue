<template>
  <b-card
    v-if="loaded"
    class="rounded-0 shadow-sm"
  >
    <slot name="card-heading" />
    <slot name="card-body" />
  </b-card>
  <b-card
    v-else
    class="rounded-0 shadow-sm"
  >
    <b-card-text class="d-flex justify-content-center card-loading">
      <!-- TODO: replace this with a cog -->
      <b-spinner
        small
        variant="secondary"
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

<style scoped>
</style>
