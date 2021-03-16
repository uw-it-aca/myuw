<template>
  <li v-if="section.sln">
      <b-link
        v-out="'Course Materials: Textbooks'"
        :href="textbookUrl"
        :title="`textbooks: ${section.curriculum_abbr} ${
          section.course_number} ${section.section_id}`"
      >Textbooks</b-link>
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
