<template>
  <uw-card-property-group>
    <uw-card-property title="Grading System">
      <span v-if="section.grading_system">
        {{titleCaseWord(section.grading_system)}}
      </span>
      <span v-else>
        Unspecified
      </span>
    </uw-card-property>
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
    </uw-card-property>

    <uw-card-property title="Grade Submission">
      <template v-if="section.gradingPeriod.isOpen">
        <div v-if="section.grading_status" class="myuw-text-md">

          <span v-if="section.grading_status === 'error'">
            <font-awesome-icon :icon="faExclamationTriangle" />
            An error occurred with
            <a href="https://gradepage.uw.edu/">Gradepage</a>. Please try again later.
          </span>

          <span v-else>
            <span v-if="section.grading_status.allGradesSubmitted && !gradeSubmittedNotAccepted">
              <a v-out="'Grade submitted'" :href="section.grading_status.section_url">
                {{section.grading_status.submitted_count}}
                grade{{section.grading_status.submitted_count ? 's' : ''}} submitted
              </a>
            </span>
            <span v-else-if="gradeSubmittedNotAccepted">
              <div class="text-danger">
                <font-awesome-icon :icon="faExclamationTriangle" />
              Grades unsuccessfully submitted
              </div>
              Error with {{section.grading_status.submitted_count}}
              grade{{section.grading_status.submitted_count ? 's' : ''}} submitted
            </span>

            <span v-if="section.grading_status.submitted_by">
              by {{section.grading_status.submitted_by}}
            </span>
            <span v-if="section.grading_status.submittedFmt" class="text-nowrap">
              on {{section.grading_status.submittedFmt}}
            </span>

            <br>
            <span v-if="gradeSubmittedNotAccepted">
              Please try
              <a
                v-out="'Grade to submit'"
                :href="section.grading_status.section_url"
              >resubmitting grades</a>
            </span>
            <span v-else-if="section.grading_status.unsubmitted_count">
              <a
                v-out="'Grade to submit'"
                :href="section.grading_status.section_url"
              >
                {{section.grading_status.unsubmitted_count}}
                grade{{section.grading_status.unsubmitted_count ? 's' : ''}}
                to submit
              </a>
            </span>
            <span v-else-if="section.is_primary_section || section.allows_secondary_grading">
              <a
                v-if="section.grading_status.no_grades_submitted"
                :href="section.grading_status.section_url"
              >
                Submit grades in Gradepage
              </a>
              <span v-else>
                {{section.grading_status.grading_status}}
              </span>
            </span>
            <span v-else>
              Grading for secondary section is disabled.
              <a :href="section.grading_status.section_url">Grade primary section</a>.
            </span>
          </span>
          <a
            v-out="'GradePage Help'"
            href="https://itconnect.uw.edu/learn/tools/gradepage/"
          >
            <font-awesome-icon :icon="faQuestionCircle" />
          </a>
        </div>

        <div class="myuw-text-sm fst-italic">
          Grade submission closes
          <strong class="fw-bold">
            {{section.gradingPeriod.deadlineFmt}}
          </strong>
          <span v-if="!section.deadline_in_24_hours">
            ({{section.gradingPeriod.deadlineRelative}})
          </span>
        </div>
      </template>

      <template v-else-if="section.gradingPeriod.isClosed">
        <div v-if="section.grading_status" class="myuw-text-md">
          <div v-if="section.grading_status.allGradesSubmitted && !gradeSubmittedNotAccepted">
            <a
              v-out="'Grade submitted by'"
              :href="section.grading_status.section_url"
            >
              {{section.grading_status.submitted_count}}
              grade{{section.grading_status.submitted_count ? 's' : ''}}
              submitted
            </a>
            <span v-if="section.grading_status.submitted_by">
              by {{section.grading_status.submitted_by}}
            </span>
            <span v-if="section.grading_status.submittedFmt" class="text-nowrap">
              on {{section.grading_status.submittedFmt}}
            </span>
            <br>
            <div>
              Grade submission for {{titleCaseWord(section.quarter)}} {{section.year}} closed
              <span class="text-nowrap">{{section.gradingPeriod.deadlineFmt}}</span>
            </div>
          </div>
          <div v-else>
            <div v-if="gradeSubmittedNotAccepted">
              <div class="text-danger">
                <font-awesome-icon :icon="faExclamationTriangle" />
                Grades unsuccessfully submitted
              </div>

              Error with {{section.grading_status.submitted_count}}
              grade{{section.grading_status.submitted_count ? 's' : ''}} submitted
              <span v-if="section.grading_status.submitted_by">
              by {{section.grading_status.submitted_by}}
              </span> on {{section.grading_status.submittedFmt}}
            </div>
            <div v-else>
              <span class="capitalize">
                {{section.grading_status.grading_status ?
                  section.grading_status.grading_status :
                  section.grading_status.unsubmitted_count
                }} grade{{section.grading_status.unsubmitted_count ? 's': ''}}
                not submitted through GradePage
              </span>
            </div>

            <div>
              Grade submission for {{titleCaseWord(section.quarter)}} {{section.year}} closed
              {{section.gradingPeriod.deadlineFmt}}
              <br>
              <a
                href="http://itconnect.uw.edu/learn/tools/gradepage/change-submitted-grades/"
              >What can I do now?</a>
            </div>
          </div>
        </div>
      </template>

      <template v-else>
        <div class="myuw-text-md">
          Grade submission opens {{section.gradingPeriod.openFmt}}
          <span v-if="!section.gradingPeriod.opensIn24Hours">
            ({{section.gradingPeriod.openRelative}})
          </span>
        </div>
        <div class="myuw-text-sm fst-italic">
          Grade submission closes
          {{section.gradingPeriod.deadlineFmt}}
        </div>
      </template>
    </uw-card-property>
  </uw-card-property-group>
</template>

<script>
import {
  faQuestionCircle,
  faExclamationTriangle
} from '@fortawesome/free-solid-svg-icons';
import CardPropertyGroup from '../../_templates/card-property-group.vue';
import CardProperty from '../../_templates/card-property.vue';

export default {
  components: {
    'uw-card-property-group': CardPropertyGroup,
    'uw-card-property': CardProperty,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      faQuestionCircle,
      faExclamationTriangle,
    }
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
        this.section.quarter, '+', this.section.year,'&sln=', this.section.sln);
        // MUWM-5145
    },
    gradeSubmittedNotAccepted() {
      return this.section.grading_status.submitted_date !== null
        && this.section.grading_status.accepted_date === null;
    }
  },
};
</script>
