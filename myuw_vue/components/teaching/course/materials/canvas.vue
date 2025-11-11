<template>
  <span>
    <a v-if="section.canvas_url"
      :href="section.canvas_url" :title="`Course Canvas of ${section.label}`"
    >Course Canvas</a>
  </span>
</template>

<script>
export default {
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
};
</script>
