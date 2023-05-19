<template>
  <uw-card-property-group>
    <uw-graading-systme :section="section"/>
    <uw-insts-of-record :section="section"/>
    <who-submits-grades :section="section"/>
    <uw-grading-delegates :section="section"/>

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
              <!-- grades have been submitted -->
              <a v-out="'Grade submitted'" :href="section.grading_status.section_url">
                {{section.grading_status.submitted_count}}
                grade{{section.grading_status.submitted_count ? 's' : ''}} submitted
              </a>
            </span>
            <span v-else-if="gradeSubmittedNotAccepted">
              <!-- grades submission unsuccessful -->
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
              Please
              <a
                v-out="'Grade to submit'"
                :href="section.grading_status.section_url"
              >try resubmitting grades</a>
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
            <span v-else-if="section.is_primary_section ||
             section.allows_secondary_grading">
              <a
                v-if="section.grading_status.no_grades_submitted"
                :href="section.grading_status.section_url"
              ><!-- grades have not been submitted yet -->
                Submit grades in Gradepage
              </a>
              <span v-else>
                <!-- Display: term grade submission opens on... -->
                {{section.grading_status.grading_status}}
                <!-- ie, term grade submission opens on... -->
              </span>
            </span>
            <span v-else>
              <!-- Section is secondary and no grading -->
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
            <!-- grades submission successful -->
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
            <div class="myuw-text-sm fst-italic">
              Grade submission for {{titleCaseWord(section.quarter)}} {{section.year}} closed
              <span class="text-nowrap">{{section.gradingPeriod.deadlineFmt}}</span>
            </div>
          </div>
          <div v-else>
            <div v-if="gradeSubmittedNotAccepted">
              <!-- grades submission unsuccessful -->
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
              <!-- grades were not submitted via GradePage -->
              <span class="capitalize">
                {{section.grading_status.grading_status ?
                  section.grading_status.grading_status :
                  section.grading_status.unsubmitted_count
                }} grade{{section.grading_status.unsubmitted_count ? 's': ''}}
                not submitted through GradePage
              </span>
            </div>
            <span class="myuw-text-sm fst-italic">
              Grade submission for {{titleCaseWord(section.quarter)}} {{section.year}} closed
              {{section.gradingPeriod.deadlineFmt}}
            </span>
            <br>
            To make changes, use <a
              href="http://itconnect.uw.edu/learn/tools/gradepage/change-submitted-grades/"
            ><em>Change Submitted Grades</em></a> form
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
import CardPropertyGroup from '../../../_templates/card-property-group.vue';
import CardProperty from '../../../_templates/card-property.vue';
import GradingSystem from './grading-system.vue';
import InstructorsOfRecord from './instructors.vue';
import WhoSubmitsGrades from './who-submit-grade.vue';
import GradiungDelegates from './delegates.vue';

export default {
  components: {
    'uw-card-property-group': CardPropertyGroup,
    'uw-card-property': CardProperty,
    'uw-graading-systme': GradingSystem,
    'uw-insts-of-record': InstructorsOfRecord,
    'who-submits-grades': WhoSubmitsGrades,
    'uw-grading-delegates': GradiungDelegates,
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
    gradeSubmittedNotAccepted() {
      return this.section.grading_status.submitted_date !== null
        && this.section.grading_status.accepted_date === null;
    },
  },
};
</script>
