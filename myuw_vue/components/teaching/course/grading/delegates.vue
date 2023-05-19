<template>
  <uw-card-property :title="`Delegate${gradeSubmissionDelegatesCount > 1 ? 's' :  ''}`">
    <ul
      v-if="section.grade_submission_delegates && section.grade_submission_delegates.length"
      class="list-unstyled mb-1"
    >
      <li
        v-for="(delegate, i) in section.grade_submission_delegates"
        :key="i"
        :class="{'mb-1': i === section.grade_submission_delegates.length + 1}"
      >
        {{titleCaseName(delegate.person.display_name)}}
        ({{titleCaseWord(delegate.level)}})
      </li>
    </ul>
    <div v-else>
      None assigned
    </div>
    <a v-if="!section.pastTerm" :href="gradeDelegateUrl" target="_blank">
      <span v-if="section.gradeSubmissionSectionDelegate">
        Update grade submission delegate
      </span>
      <span v-else>
        Add grade submission delegate
      </span>
    </a>
    <div>
      <span class="myuw-text-sm fst-italic">
      In an emergency, delegates can submit grades if instructors of record cannot.
      </span>
      <uw-collapsed-item :part="gradingDelegateLearnMore" caller-id="GradingDelegates">
        <template #collapsed-body>
          Grading delegates ...
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
    gradingDelegateLearnMore() {
      return {
        title: 'Learn more',
        id: 'gradingDelegateLearnMore' + this.section.sln,
      };
    },
  },
};
</script>
