<template>
  <uw-card-property title="Who Submits Grades">
    <div>
      <span v-if="secondarySubmitsGrades">Either linked or primary section instructor(s)</span>
      <span v-else>Primary section instructor</span>
    </div>
    <div>
      <span class="myuw-text-sm fst-italic">
        <span v-if="secondarySubmitsGrades">
          Both linked section and primary section instructors
        </span>
        <span v-else>
          Only primary section instructor
        </span>
        of record will be able to submit grades through GradePage.
      </span>
      <uw-collapsed-item
        v-if="!section.pastTerm"
        :part="whoSubmitsGrades"
        caller-id="WhoSubmitsGrades"
      >
        <template #collapsed-body>
          Correctly configured courses allow linked section instructors (usually TAs) to submit
          grades through GradePage. Otherwise, only primary section instructors can submit grades.
          <br>
          <br>To change who can submit grades, contact the registrar at
          <a href="mailto:registra@uw.edu?subject=Grade submission help">registra@uw.edu</a>.
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
