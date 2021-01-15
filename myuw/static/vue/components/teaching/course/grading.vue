<template>
  <div>
    <h5 :class="{'sr-only': showRowHeader}">
      Grading System
    </h5>
    <div>
      <span v-if="section.grading_system">
        {{titleCaseWord(section.grading_system)}}
      </span>
      <span v-else>
        Unspecified
      </span>
    </div>
    <h5 :class="{'sr-only': showRowHeader}">
      Delegate{{gradeSubmissionDelegatesCount > 1 ? 's' :  ''}}
    </h5>
    <div>
      <ul v-if="section.grade_submission_delegates">
        <li v-for="(delegate, i) in section.grade_submission_delegates" :key="i">
          {{titleCaseName(delegate.person.display_name)}}
          ({{titleCaseWord(delegate.level)}})
        </li>
      </ul>
      <span v-else>
        None assigned
      </span>
      <a
        :href="`https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/pop/gradedelegate.aspx?quarter=${section.quarter}+${section.year}&sln=${section.sln}&chanid=11`"
        :label="(section.gradeSubmissionSectionDelegate ? 'Update' : 'Add')
          + `Grading Delegate: ${section.curriculum_abbr} ${
            section.course_number} ${section.section_id}`"
      >
        <span v-if="section.gradeSubmissionSectionDelegate">
          Update grade submission delegate
        </span>
        <span v-else>
          Add grade submission Delegate
        </span>
      </a>
    </div>
    <h5 :class="{'sr-only': showRowHeader}">
      Grade Submission
    </h5>
    <div>
      <div v-if="section.gradingPeriod.isOpen">
        <div v-if="section.grading_status !== 'error'">
          <span v-if="section.grading_status">
            <span v-if="section.grading_status.allGradesSubmitted">
              <a
                :href="section.grading_status.section_url"
                :label="`GradePage ${section.curriculum_abbr} ${
                  section.course_number
                } ${section.section_id}`"
                target="_blank"
              >
                {{section.grading_status.submitted_count}}
                grade{{section.grading_status.submitted_count ? 's' : ''}}
                submitted
              </a>
               by {{section.grading_status.submitted_by}} on
              <span>{{section.grading_status.submittedFmt}}</span>
            </span>
            <span v-else-if="section.grading_status.unsubmitted_count">
              <a
                :href="section.grading_status.section_url"
                :label="`GradePage ${section.curriculum_abbr} ${
                  section.course_number
                } ${section.section_id}`"
                target="_blank"
              >
                {{section.grading_status.unsubmitted_count}}
                grade{{section.grading_status.unsubmitted_count ? 's' : ''}}
                to submit
              </a>
            </span>
            <span v-else-if="
              section.is_primary_section ||
              section.allows_secondary_grading
            ">
              <a
                v-if="section.grading_status.no_grades_submitted"
                :href="section.grading_status.section_url"
                :label="`GradePage ${section.curriculum_abbr} ${
                  section.course_number
                } ${section.section_id}`"
                target="_blank"
              >
                Submit grades in Gradepage
              </a>
              <span v-else>
                {{section.grading_status.grading_status}}
              </span>
            </span>
            <span v-else>
              Grading for secondary section is disabled.
              <a
                :href="section.grading_status.section_url"
                :label="`GradePage ${section.curriculum_abbr} ${
                  section.course_number
                } ${section.section_id}`"  target="_blank">
                Grade primary section
              </a>.
            </span>
          </span>
          <a
            href="https://itconnect.uw.edu/learn/tools/gradepage/"
            target="_blank" 
            label="GradePage Help"
          >
            <font-awesome-icon :icon="faQuestionCircle" />
          </a>
        </div>
        <div v-else>
          <font-awesome-icon :icon="faExclamationTriangle" />
          An error occurred with
          <a
            href="https://gradepage.uw.edu/"
            label="Gradepage"
            target="_blank"
          >
            Gradepage
          </a>. Please try again later.
        </div>
        Grade submission closes
        <strong>
          {{section.gradingPeriod.deadlineFmt}}
        </strong>
        <span v-if="!section.deadline_in_24_hours">
          ({{section.gradingPeriod.deadlineRelative}})
        </span>
      </div>
      <div v-else-if="section.gradingPeriod.isClosed">
        <div v-if="section.grading_status">
          <span v-if="section.grading_status.allGradesSubmitted">
            <a
              :href="section.grading_status.section_url"
              :label="`GradePage ${section.curriculum_abbr} ${
                section.course_number
              } ${section.section_id}`"
              target="_blank"
            >
              {{section.grading_status.submitted_count}}
              grade{{section.grading_status.submitted_count ? 's' : ''}}
              submitted by {{section.grading_status.submitted_by}} on 
            </a>
            <span>{{section.grading_status.submittedFmt}}</span>
            <div>
              Grade submission for {{titleCaseWord(section.quarter)}} {{section.year}} closed
              <span>{{section.gradingPeriod.deadlineFmt}}</span>
            </div>
          </span>
        </div>
        <div v-else>
          <span v-if="section.grading_status">
            {{section.grading_status.grading_status ?
              section.grading_status.grading_status :
              section.grading_status.unsubmitted_count
            }} grade{{section.grading_status.unsubmitted_count ? 's': ''}}
            not submitted through GradePage
          </span>
          <div>
            Grade submission for {{titleCaseWord(section.quarter)}} {{section.year}} closed
            {{section.gradingPeriod.deadlineFmt}}
            <span v-if="section.grading_status">
              <br />
              <a
                href="http://itconnect.uw.edu/learn/tools/gradepage/change-submitted-grades/"
                label="Change Submitted Grades"
                target="_blank"
              >What can I do now?</a>
            </span>
          </div>
        </div>
      </div>
      <div v-else>
        <div>
          Grade submission opens {{section.gradingPeriod.openFmt}}
          <span v-if="!section.gradingPeriod.opensIn24Hours">
            ({{section.gradingPeriod.openRelative}})
          </span>
        </div>
        <div>
          Grade submission closes
          {{section.gradingPeriod.deadlineFmt}}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  faQuestionCircle,
  faExclamationTriangle
} from '@fortawesome/free-solid-svg-icons';

export default {
  props: {
    section: {
      type: Object,
      required: true,
    },
    showRowHeader: {
      type: Boolean,
      default: false,
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
    }
  }
};
</script>
