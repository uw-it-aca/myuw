<template>
    <uw-card-property title="Primary or Secondary">
      <div>
        <span v-if="allowSecondaryGrading">Secondary</span>
        <span v-else>Primary</span>
      </div>
      <div>
        <span class="myuw-text-sm fst-italic">
          Only
          <span v-if="allowSecondaryGrading">secondary</span><span v-else>primary</span>
          (section) instructors of record can submit grades.
        </span>
        <uw-collapsed-item
          :part="secondaryGrading" caller-id="AllowSecondaryGrading">
          <template #collapsed-body>
            When ...
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
    allowSecondaryGrading() {
      return this.section.allows_secondary_grading;
    },
    secondaryGrading () {
      return {
        title: 'Learn more',
        id: 'secondaryGradingLearnMore' + this.section.sln,
      };
    },
  },
};
</script>
