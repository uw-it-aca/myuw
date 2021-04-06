<template>
  <li v-if="section.canvas_url">
    <span>
      <a v-if="section.canvas_url === 'error'"
        href="https://canvas.uw.edu/"
        target="_blank"
      >Canvas LMS Home page</a>

      <a v-else
        :href="section.canvas_url"
        :title="`Course Canvas of ${section.label}`"
        target="_blank"
      >Course Canvas</a>
    </span>
  </li>
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
