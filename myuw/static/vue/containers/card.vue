<template>
  <b-card v-if="loaded">
    <slot name="card-heading"></slot>
    <slot name="card-body"></slot>
  </b-card>
  <b-card v-else>
    <b-card-text class="d-flex justify-content-center card-loading">
      <!-- TODO: replace this with a cog -->
      <b-spinner class="my-auto" label="Loading..."></b-spinner>
    </b-card-text>
  </b-card>
</template>

<script>

export default {
  props: {
    loaded: {
      type: Boolean,
      default: false,
    }
  },
  data: function () {
    return {};
  },
};
</script>

<style scoped>
</style>
