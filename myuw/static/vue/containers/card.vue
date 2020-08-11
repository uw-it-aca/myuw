<template>
  <b-card v-if="loaded">
    <h3><slot name="card-heading"></slot></h3>
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
  .card {
    border-radius: 0;
    border: 1px solid #ddd;
    box-shadow: 0 1px 3px rgba(34, 25, 25, 0.15);
  }
  .card-body {
    padding: 16px;
  }
  h3 {
    font-weight: 600;
    color: #85754d;
  }
  .card-loading {
    min-height: 60px;
    color: #ddd;
  }
</style>
