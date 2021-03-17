<template>
  <div>
    <h5 class="sr-only">Course Resources</h5>
    <div>
      <ul class="list-unstyled myuw-text-md mb-0">
        <template v-if="hasResources">
          <li v-if="section.class_website_url" class="mb-1">
            <a
              v-out="`Course Website ${section.id}`"
              :href="section.class_website_url"
              :title="`Course Website ${section.id}`"
            >
              Course Website
            </a>
          </li>
          <li v-if="section.lib_subj_guide" class="mb-1">
            <a
              v-out="`Library Research Guides: ${section.id}`"
              :href="section.lib_subj_guide"
              :title="`Library Research Guides ${section.id}`"
            >
              Library Research Guides
            </a>
          </li>
          <li v-if="section.canvas_url" class="mb-1">
            <a
              v-out="`Course Canvas ${section.id}`"
              :href="section.canvas_url"
              :title="`Course Canvas ${section.id}`"
            >
              Course Canvas
            </a>
          </li>
        </template>
        <li v-if="section.sln" class="mb-1">
          <a
            v-inner="`Textbooks ${section.id}`"
            :href="textbookHref"
            :title="`Textbooks ${section.id}`"
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
  },
  computed: {
    textbookHref() {
      let url = `/textbooks/${this.section.year},${this.section.quarter}`;

      if (this.section.requestSummerTerm) {
        url += `,${this.section.requestSummerTerm.toLowerCase()}`;
      }
      url += `/${this.section.curriculum_abbr}${
        this.section.course_number
      }${this.section.section_id}`;

      return url;
    },
    hasResources() {
      return (
        this.section.class_website_url ||
        this.section.lib_subj_guide ||
        this.section.canvas_url
      );
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
