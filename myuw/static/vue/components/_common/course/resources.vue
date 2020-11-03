<template>
  <b-col>
    <h5 class="h6 font-weight-bold text-danger">Course Resources</h5>
    <ul class="list-unstyled myuw-text-md">
      <li v-if="section.class_website_url" class="mb-1">
        <a
          :href="section.class_website_url"
          :label="`${
            section.curriculum_abbr
          } ${section.course_number} Course Website`"
        >
          Course Website
        </a>
      </li>
      <li v-if="section.lib_subj_guide" class="mb-1">
        <a
          :href="section.lib_subj_guide"
          :label="`${
            section.curriculum_abbr
          } ${section.course_number} Library Research Guides`"
        >
          Library Research Guides
        </a>
      </li>
      <li v-if="section.canvas_url" class="mb-1">
        <a
          :href="section.canvas_url"
          :label="`${
            section.curriculum_abbr
          } ${section.course_number} Course Canvas`"
        >
          Course Canvas
        </a>
      </li>
      <li v-if="section.sln" class="mb-1">
        <a
          :href="slnHref"
          :label="`${
            section.curriculum_abbr
          } ${section.course_number} Course Canvas`"
        >
          Textbooks
        </a>
      </li>
    </ul>
  </b-col>
</template>

<script>
export default {
  props: {
    section: {
      type: Object,
      required: true,
    },
    course: {
      type: Object,
      required: true,
    },
  },
  computed: {
    slnHref() {
      let url = `/textbooks/${this.course.year},${this.course.quarter}`;

      if (this.course.summer_term) {
        url += `,${this.course.summer_term.toLowerCase()}`;
      }
      url += `/${this.section.curriculum_abbr}${
        this.section.course_number
      }${this.section.section_id}`;

      return url;
    },
  },
};
</script>

<style lang="scss" scoped>
tr {
  td:not(:first-child) {
    text-align: center;
  }
}
</style>
