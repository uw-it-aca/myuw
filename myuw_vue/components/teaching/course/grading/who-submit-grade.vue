<template>
    <uw-card-property title="Who submits grades">
      <div>
        <span v-if="secondarySubmitsGrades">Linked section instructor(s)</span>
        <span v-else>Primary section instructor</span>
      </div>
      <div>
        <span class="myuw-text-sm fst-italic">
          Only
          <span v-if="secondarySubmitsGrades">
            linked section instructor(s)
          </span><span v-else>
            primary section instructor
          </span> of record will be able to submit grades through GradePage.
        </span>
        <uw-collapsed-item
          :part="whoSubmitsGrades" caller-id="WhoSubmitsGrades">
          <template #collapsed-body>
            Either ...
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
    'uw-collapsed-item': CollapsedItem
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
  computed: {
    secondarySubmitsGrades() {
      return this.section.allows_secondary_grading;
    },
    whoSubmitsGrades () {
      return {
        title: 'Learn more',
        id: 'whoSubmitsGradesLearnMore' + this.section.sln,
      };
    },
  },
};
</script>
