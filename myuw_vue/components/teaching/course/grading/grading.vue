<template>
  <uw-card-property-group>
    <uw-graading-systme :section="section"/>
    <uw-insts-of-record
      v-if="section.instructors.length > 0" :section="section"/>
    <who-submits-grades :section="section"/>
    <uw-grading-delegates
      v-if="section.grade_submission_delegates.length > 0" :section="section"/>
    <uw-grade-submission :section="section"/>
  </uw-card-property-group>
</template>

<script>
import CardPropertyGroup from '../../../_templates/card-property-group.vue';
import GradingSystem from './grading-system.vue';
import InstructorsOfRecord from './instructors.vue';
import WhoSubmitsGrades from './who-submit-grade.vue';
import GradiungDelegates from './delegates.vue';
import GradeSubmission from './submission.vue';

export default {
  components: {
    'uw-card-property-group': CardPropertyGroup,
    'uw-graading-systme': GradingSystem,
    'uw-insts-of-record': InstructorsOfRecord,
    'who-submits-grades': WhoSubmitsGrades,
    'uw-grading-delegates': GradiungDelegates,
    'uw-grade-submission': GradeSubmission,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
};
</script>
