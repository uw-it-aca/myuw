<template>
  <uw-card-property
    v-if="notInPerson"
    title="Course Mode"
    :sr-only-title="!showRowHeading"
  >
    <uw-course-mode
      :section="section"
      :include-t-s-c="showRowHeading"
      :hide-info-link="hideInfoLink"/>
  </uw-card-property>
</template>

<script>
import CardProperty from '../../../_templates/card-property.vue';
import CourseMode from './mode.vue';
export default {
  components: {
    'uw-card-property': CardProperty,
    'uw-course-mode': CourseMode,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
    showRowHeading: {
      type: Boolean,
      default: false,
    },
    hideInfoLink: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    notInPerson() {
      // MUWM-5210
      return (
        this.section.is_asynchronous ||
        this.section.is_synchronous ||
        this.section.is_hybrid);
    }
  },
};
</script>
