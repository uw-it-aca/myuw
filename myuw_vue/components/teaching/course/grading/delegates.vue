<template>
  <uw-card-property :title="`Delegate${gradeSubmissionDelegatesCount > 1 ? 's' : ''}`">
    <ul
      v-if="section.grade_submission_delegates && section.grade_submission_delegates.length"
      class="list-unstyled mb-1"
    >
      <li
        v-for="(delegate, i) in section.grade_submission_delegates"
        :key="i"
        :class="{ 'mb-1': i === section.grade_submission_delegates.length + 1 }"
      >
        {{ titleCaseName(delegate.person.display_name) }}
        ({{ titleCaseWord(delegate.level) }})
      </li>
    </ul>
    <div v-else>None assigned</div>
    <div>
      <span class="myuw-text-sm fst-italic">
        In an emergency, delegates can submit grades if instructors of record cannot.
      </span>
      <uw-collapsed-item :part="gradingDelegateLearnMore" caller-id="GradingDelegates">
        <template #collapsed-body>
          Grading delegates provide an alternative in case the official Instructor of Record (IoR)
          is unable to submit grades for any reason. You can 
          <a v-if="!section.pastTerm" :href="gradeDelegateUrl" target="_blank">
            <span v-if="section.gradeSubmissionSectionDelegate">
              update grade submission delegates
            </span>
            <span v-else> add a grade submission delegate </span>
          </a>
          using MyClass Resources.
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
    gradeSubmissionDelegatesCount() {
      if (this.section.grade_submission_delegates) {
        return this.section.grade_submission_delegates.length;
      }
      return 0;
    },
    gradeDelegateUrl() {
      return ''.concat(
        'https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/pop/gradedelegate.aspx?quarter=',
        this.section.quarter,
        '+',
        this.section.year,
        '&sln=',
        this.section.sln
      );
      // MUWM-5145
    },
    gradingDelegateLearnMore() {
      return {
        title: 'Learn more',
        id: 'gradingDelegateLearnMore' + this.section.sln,
      };
    },
  },
};
</script>
