<template>
  <span v-if="section.canvas_url">
    <a v-if="section.canvas_url === 'error'"
      href="https://canvas.uw.edu/"
    >Canvas LMS Home page</a>

    <a v-else
      :href="section.canvas_url"
      :title="`Course Canvas of ${section.label}`"
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
