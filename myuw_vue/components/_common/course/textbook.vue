<template>
  <a
    :href="uwtCourse ? uwtTextbookUrl : textbookPageUrl"
    :title="`Textbooks of ${section.label}`"
  >Textbooks</a>
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
    termId() {
      if (this.section.quarter.toLowerCase() === "winter") return "1";
      if (this.section.quarter.toLowerCase() === "spring") return "2";
      if (this.section.quarter.toLowerCase() === "summer") return "3";
      return "4";
    },
    uwtTextbookUrl() {
      // MUWM-5311
      return (
        "https://www.bkstr.com/webApp/discoverView?" +
        "bookstore_id-1=2335&div-1=&termid-1=" + 
         String(this.section.year) + this.termId +
        "&dept-1=" + encodeURIComponent(this.section.curriculum_abbr) +
        "&course-1=" + this.section.course_number +
        "&section-1=" + this.section.section_id);
    },
    uwtCourse() {
      return this.section.course_campus.toLowerCase() === 'tacoma';
    },
    textbookPageUrl() {
      let url = `/textbooks/${this.section.year},${this.section.quarter}`;

      if (this.section.requestSummerTerm) {
        url += `,${this.section.requestSummerTerm.toLowerCase()}`;
      }
      url += (
        '#' + this.section.curriculum_abbr +
        this.section.course_number + this.section.section_id);

      return url;
    },
  },
};
</script>
