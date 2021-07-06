<template>
  <b-link
    v-if="section.sln"
    :href="textbookUrl"
    :title="`Textbooks of ${section.label}`"
  >
    Textbooks
  </b-link>
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
      let url = "/textbooks/" + this.section.year + ',' + this.section.quarter;
      if (this.section.summer_term) {
        url = url + ',' + this.section.summer_term.toLowerCase();
      }
      return url + '#' + this.section.curriculum_abbr +
        this.section.course_number + this.section.section_id;
    }
  },
};
</script>
