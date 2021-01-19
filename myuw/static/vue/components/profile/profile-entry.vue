<template>
  <b-row>
    <b-col :sm="titleWidth">
      <h4 class="h4 font-weight-bold myuw-text-md">
        {{ title }}
      </h4>
    </b-col>
    <b-col :sm="contentWidth">
      <slot name="content">
        {{ content }}
      </slot>
    </b-col>
  </b-row>
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
  data: function() {
    return {
      titleWidth: 3,
      contentWidth: 9,
    }
  },
};
</script>

<style lang="scss" scoped>

</style>
