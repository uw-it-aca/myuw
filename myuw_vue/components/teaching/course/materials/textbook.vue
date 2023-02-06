<template>
  <a
    v-if="section.sln"
    :href="textbookUrl"
    :title="`Textbooks of ${section.label}`"
  >
    Textbooks
  </a>
</template>

<script>
export default {
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
  computed: {
    textbookUrl() {
      return (
        "/textbooks/" + this.section.year + ',' + this.section.quarter + '#' +
        this.section.curriculum_abbr + this.section.course_number + this.section.section_id
      );
    }
  },
};
</script>
