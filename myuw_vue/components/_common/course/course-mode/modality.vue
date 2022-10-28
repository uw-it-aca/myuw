<template>
  <uw-card-property title="Course Mode" :sr-only-title="!showRowHeading">
    <uw-cmode
      :section="section"
      :include-t-s-c="showRowHeading"
      :hide-info-link="hideInfoLink"/>
  </uw-card-property>
</template>

<script>
import CardProperty from '../../../_templates/card-property.vue';
import Mode from './mode.vue';
export default {
  components: {
    'uw-card-property': CardProperty,
    'uw-cmode': Mode,
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
