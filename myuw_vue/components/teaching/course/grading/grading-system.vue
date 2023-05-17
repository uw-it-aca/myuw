<template>
    <uw-card-property title="Grading System">
      <span v-if="section.grading_system">
        {{titleCaseWord(section.grading_system)}}
      </span>
      <span v-else>
        Unspecified
      </span>
      <div>
        Grading systems: Standard or Credit/No-Credit
        <uw-collapsed-item
          :part="gradingLearnMore" caller-id="GradingSystem">
          <template #collapsed-body>
            To change ...
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
        title: "Learn more",
        id: "gradingLearnMore" + this.section.sln,
      };
    }
  },
};
</script>
