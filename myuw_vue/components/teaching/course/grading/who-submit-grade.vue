<template>
  <uw-card-property title="Who Submits Grades">
    <div>
      <span v-if="secondarySubmitsGrades">Linked section instructor(s)</span>
      <span v-else>Primary section instructor</span>
    </div>
    <div>
      <span class="myuw-text-sm fst-italic">
        Only
        <span v-if="secondarySubmitsGrades">
          linked section instructor(s)
        </span>
        <span v-else>
          the primary section instructor
        </span>
        of record will be able to submit grades through GradePage.
      </span>
      <uw-collapsed-item :part="whoSubmitsGrades" caller-id="WhoSubmitsGrades">
        <template #collapsed-body>
          Either primary section instructors <b>OR</b> linked section instructors (usually TAs)
          can submit grades through GradePage.
          <br>
          <br>To change who can submit grades,
          <a href="mailto:registra@uw.edu?subject=Grade submission help">contact the registrar</a>.
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
    secondarySubmitsGrades() {
      return this.section.allows_secondary_grading;
    },
    whoSubmitsGrades() {
      return {
        title: 'Learn more',
        id: 'whoSubmitsGradesLearnMore' + this.section.sln,
      };
    },
  },
};
</script>
