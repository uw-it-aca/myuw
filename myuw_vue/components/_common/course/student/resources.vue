<template>
  <div>
    <h3 class="visually-hidden">Course Resources</h3>
    <div>
      <ul class="list-unstyled myuw-text-md mb-0">
        <template v-if="hasResources">
          <li v-if="section.class_website_url" class="mb-1">
            <a
              :href="section.class_website_url"
              :title="`Course Website of ${section.label}`"
            >
              Course Website
            </a>
          </li>
          <li v-if="section.lib_subj_guide" class="mb-1">
            <a
              :href="section.lib_subj_guide"
              :title="`Library Research Guides of ${section.label}`"
            >
              Library Research Guides
            </a>
          </li>
          <li v-if="section.canvas_url" class="mb-1">
            <a
              :href="section.canvas_url"
              :title="`Course Canvas of ${section.label}`"
            >
              Course Canvas
            </a>
          </li>
        </template>
        <li v-if="section.sln" class="mb-1">
          <uw-textbook :section="section" />
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import TextbookPanel from '../textbook.vue';
export default {
  components: {
    'uw-textbook': TextbookPanel,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
  computed: {
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
