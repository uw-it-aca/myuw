<template>
  <b-row>
    <b-col :sm="titleWidth">{{ title }}</b-col>
    <b-col :sm="contentWidth">
      <slot name="content">
        {{ content }}
      </slot>
    </b-col>
  </b-row>
</template>

<script>
export default {
  data: function() {
    return {
      titleWidth: 3,
      contentWidth: 9,
    }
  },
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
};
</script>

<style lang="scss" scoped>

</style>
