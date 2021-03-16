<template>
  <li v-if="section.canvas_url">
    <span>
      <a v-if="section.canvas_url === 'error'"
        v-out="'Canvas LMS'"
        href="https://canvas.uw.edu/"
        target="_blank"
      >Canvas LMS Home page</a>

      <a v-else
        v-out="'Course Materials: Canvas'"
        :href="section.canvas_url"
        :title="`course: ${section.curriculum_abbr} ${
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
