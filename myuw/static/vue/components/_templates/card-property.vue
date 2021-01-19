<template>
  <div class="d-md-flex mb-3 myuw-text-md">
    <div class="flex-md-fill mr-3 bd-highlight font-weight-bold property-label">
      {{ title }}
    </div>
    <div class="flex-md-fill">
      <slot name="content">
        {{ content }}
      </slot>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true,
    },
    content: {
      type: String,
      required: false,
      default: null,
    },
  },
  data: function () {
    return {};
  },
};
</script>

<style lang="scss" scoped>
@media (min-width: 768px) {
  .property-label {
    min-width: 25%;
    max-width: 25%;
  }
}
</style>
