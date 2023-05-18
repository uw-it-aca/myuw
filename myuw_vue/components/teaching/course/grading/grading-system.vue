<template>
  <uw-card-property title="Grading System">
    <span v-if="section.grading_system">
      {{ titleCaseWord(section.grading_system) }}
    </span>
    <span v-else> Unspecified </span>
    <div>
      <span class="myuw-text-sm fst-italic">Grading systems: Standard or Credit/No-Credit</span>
      <uw-collapsed-item :part="gradingLearnMore" caller-id="GradingSystem">
        <template #collapsed-body>
          To change your
          <a href="https://www.washington.edu/students/gencat/front/Grading_Sys.html"
          >grading system</a>, contact your departmental time schedule coordinator.
        </template>
      </uw-collapsed-item>
    </div>
  </uw-card-property>
</template>

<script>
import CardProperty from '../../../_templates/card-property.vue';
import CollapsedItem from '../../../_common/collapsed-part.vue';

export default {
  components: {
    'uw-card-property': CardProperty,
    'uw-collapsed-item': CollapsedItem,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
  computed: {
    gradingLearnMore() {
      return {
        title: 'Learn more',
        id: 'gradingLearnMore' + this.section.sln,
      };
    },
  },
};
</script>
