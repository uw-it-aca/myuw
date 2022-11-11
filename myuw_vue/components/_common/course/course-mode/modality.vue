<template>
  <uw-card-property title="Course Mode" :sr-only-title="!showRowHeading">
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
};
</script>
