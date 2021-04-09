<template>
  <div class="d-md-flex mb-3 myuw-text-md">
    <slot name="title">
      <div class="text-dark-beige flex-md-fill mr-3 bd-highlight
        myuw-font-encode-sans property-label">
        {{ title }}
      </div>
    </slot>
    <div class="flex-md-fill">
      <slot></slot>
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
