<template>
  <div class="d-flex">
    <h5 :class="[!showRowHeading ? 'sr-only' : '']"
        class="w-25 font-weight-bold myuw-text-md"
    >
      Course Resources
    </h5>
    <div class="flex-fill">
      <ul class="list-unstyled myuw-text-md mb-0">
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
    </div>
  </div>
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
    showRowHeading: {
      type: Boolean,
      default: false,
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
