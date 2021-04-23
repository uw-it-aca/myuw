<template>
  <div class="card-property d-md-flex myuw-text-md" :class="{'mb-2': !noMarginBottom}">
    <slot name="title">
      <h3
        v-if="title.length > 0"
        class="h6 flex-md-fill mr-3 mb-0 bd-highlight myuw-font-encode-sans property-label"
        :class="{'sr-only': srOnlyTitle}"
      >
        {{ title }}
      </h3>
      <span v-else class="flex-md-fill mr-3 property-label"/>
    </slot>
    <div class="property-content flex-md-fill">
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
    srOnlyTitle: {
      type: Boolean,
      default: false,
    },
    noMarginBottom: {
      type: Boolean,
      default: false,
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
    color: #333;

  }
}
</style>
