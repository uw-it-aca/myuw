<template>
  <li v-if="section.canvas_url">
    <span>
      <a v-if="section.canvas_url === 'error'"
        href="https://canvas.uw.edu/"
        label="Canvas LMS"
        target="_blank"
      >Canvas LMS Home page</a>

      <a v-else
        :href="section.canvas_url"
        :label="`Course Canvas: ${section.curriculum_abbr} ${
          section.course_number} ${section.section_id}`"
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
