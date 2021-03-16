<template>
  <div>
    <h5 :class="{'sr-only': showRowHeader}">
      Evaluations
    </h5>
    <div>
      <ul>
        <template v-if="section.evaluation && section.evaluation.eval_status">
          <template v-if="section.evaluation.is_online">
            <template v-if="section.evaluation.eval_open_date">
              <template v-if="section.evaluation.is_closed">
                <li>
                  <span>
                    Closed
                    {{section.evaluation.evalCloseDateDisplay}}
                    <span v-if="section.evaluation.responseRatePercent">
                      with a {{section.evaluation.responseRatePercent}}%
                      response rate.
                    </span>
                  </span>
                </li>
                <li v-if="section.evaluation.report_url">
                  <a
                    v-out="`View evaluation report ${section.section_label}`"
                    :href="section.evaluation.report_url"
                    :title="`${section.section_label} Course Evaluation Report`"
                  >
                    View evaluation results report
                  </a>
                </li>
              </template>
              <template v-if="section.evaluation.is_open">
                <li>
                  <span>
                    Open:&nbsp;&nbsp;{{section.evaluation.responseRatePercent}}%
                    of responses received
                  </span>
                  <p class="myuw-note">
                    Closes {{section.evaluation.evalCloseDateDisplay}}
                  </p>
                </li>
                <li>
                  <span>
                    Results:&nbsp;&nbsp;Report will be available
                    {{section.evaluation.reportAvailableDateDisplay}}
                  </span>
                </li>
                <li>
                  <a
                    v-out="`Manage evaluation of ${section.section_label}`"
                    :href="`https://${section.evaluation.domain}.iasystem.org/faculty`"
                    :title="`${section.section_label} Course Evaluation`"
                  >Manage evaluation</a>
                </li>
              </template>
              <template v-if="section.evaluation.is_pending">
                <li>
                  Online evaluation will open {{section.evaluation.evalOpenDateDisplay}}
                </li>
                <li>
                  <a
                    v-out="`Manage evaluation of ${section.section_label}`"
                    :href="`https://${section.evaluation.domain}.iasystem.org/faculty`"
                    :title="`${section.section_label} Course Evaluation`"
                  >Manage evaluation</a>
                </li>
              </template>
            </template>
            <template v-else>
              <li v-if="section.evaluation.report_available_date">
                Report Available
                {{section.evaluation.reportAvailableDateDisplay}}
              </li>
              <li v-if="section.evaluation.report_url">
                <a
                  v-out="`View evaluation report ${section.section_label}`"
                  :href="section.evaluation.report_url"
                  :title="`${section.section_label} Course Evaluation Report`"
                >
                  View evaluation results report
                </a>
              </li>
              <li>
                <strong>
                  {{section.evaluation.responseRatePercent}}% Response rate
                </strong>
              </li>
            </template>
          </template>
          <template v-else>
            <li>
              Paper-based evaluation
            </li>
            <li>
              <a
                v-out="`Manage evaluation of ${section.section_label}`"
                :href="`https://${section.evaluation.domain}.iasystem.org/faculty`"
                :title="`${section.section_label} Course Evaluation`"
              >Manage evaluation</a>
            </li>
          </template>
        </template>
        <template v-else>
          <li v-if="section.evaluation && section.evaluation.eval_not_exist">
            You {{section.pastTerm ? 'did' : 'do'}}
            not have an evaluation set up for this course.
            <a v-out="'Learn About Course Evaluations'"
               href="https://www.washington.edu/assessment/course-evaluations/"
               target="_blank"
            ><font-awesome-icon :icon="faQuestionCircle" /></a>
          </li>
          <li v-else>
            <font-awesome-icon :icon="faExclamationTriangle" />
            An error occurred with the course evaluation. Please try again later.
          </li>
        </template>
      </ul>
    </div>
  </div>
</template>

<script>
import {
  faQuestionCircle,
  faExclamationTriangle,
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
}
</script>