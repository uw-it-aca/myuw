<template>
  <uw-card 
    v-if="!loaded || sectionData.current"
    :loaded="loaded"
    no-bottom-margin
    class="statistics-card mb-0"
  >
    <template #card-heading>
      <h3 class="h5 text-dark-beige myuw-font-encode-sans">
        Statistics for
        {{ sectionData.currAbbr }} {{ sectionData.courseNum }} {{ sectionData.sectionId }}
      </h3>
    </template>
    <template #card-body>
      <p v-if="majors && majors.length">
        {{ majors[0].percent_students }}% of your students
        are {{ titleCaseWord(majors[0].major) }} majors.
      </p>
      <a v-out="'Course Dashboard'" :href="url" target="_blank" :title="label">
        View more statistics for
        {{ sectionData.currAbbr }} {{ sectionData.courseNum }} {{ sectionData.sectionId }}
      </a>
    </template>
  </uw-card>
</template>

<script>
import Card from '../../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  props: {
    loaded: {
      type: Boolean,
      required: true,
    },
    sectionData: {
      type: Object,
      required: true,
    },
  },
  computed: {
    url() {
      return `https://coda.uw.edu/#${this.sectionData.year}-` +
             `${this.sectionData.quarter}-${this.sectionData.currAbbr}-` +
             `${this.sectionData.courseNum}-${this.sectionData.sectionId}`;
    },
    label() {
      return `Course Dashboard for ${this.sectionData.year} ${this.sectionData.quarter} ` +
             `${this.sectionData.currAbbr} ${this.sectionData.courseNum} ` +
             `${this.sectionData.sectionId}`;
    },
    majors() {
      return this.sectionData.sections[0].current_student_majors;
    }
  },
};
</script>

<style lang="scss" scoped>
.statistics-card {
  position: sticky;
  bottom: 0;
  float: right;
  max-width: 285px
}
</style>
