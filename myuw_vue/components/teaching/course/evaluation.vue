<template>
  <uw-card-property-group>
    <uw-card-property title="Evaluations" :no-margin-bottom="noMarginBottom">
      <ul class="mb-0 list-unstyled">
        <template v-if="section.evaluation && section.evaluation.eval_status">
          <template v-if="section.evaluation.is_online">
            <template v-if="section.evaluation.eval_open_date">
              <template v-if="section.evaluation.is_closed">
                <li class="mb-1">
                  <span>
                    Closed
                    {{section.evaluation.evalCloseDateDisplay}}
                    <span v-if="section.evaluation.responseRatePercent">
                      with a {{section.evaluation.responseRatePercent}}%
                      response rate.
                    </span>
                  </span>
                </li>
                <li v-if="section.evaluation.report_url" class="mb-1">
                  <a :href="section.evaluation.report_url">
                    View evaluation results report
                  </a>
                </li>
              </template>
              <template v-if="section.evaluation.is_open">
                <li class="mb-1">
                  <span>
                    Open:&nbsp;&nbsp;{{section.evaluation.responseRatePercent}}%
                    of responses received
                  </span>
                  <p class="myuw-note">
                    Closes {{section.evaluation.evalCloseDateDisplay}}
                  </p>
                </li>
                <li class="mb-1">
                  <span>
                    Results:&nbsp;&nbsp;Report will be available
                    {{section.evaluation.reportAvailableDateDisplay}}
                  </span>
                </li>
                <li class="mb-1">
                  <a
                    :href="`https://${section.evaluation.domain}.iasystem.org/faculty`"
                  >Manage evaluation</a>
                </li>
              </template>
              <template v-if="section.evaluation.is_pending">
                <li class="mb-1">
                  Online evaluation will open {{section.evaluation.evalOpenDateDisplay}}
                </li>
                <li class="mb-1">
                  <a
                    :href="`https://${section.evaluation.domain}.iasystem.org/faculty`"
                  >Manage evaluation</a>
                </li>
              </template>
            </template>
            <template v-else>
              <li v-if="section.evaluation.report_available_date" class="mb-1">
                Report Available
                {{section.evaluation.reportAvailableDateDisplay}}
              </li>
              <li v-if="section.evaluation.report_url" class="mb-1">
                <a :href="section.evaluation.report_url">
                  View evaluation results report
                </a>
              </li>
              <li class="mb-1">
                <strong>
                  {{section.evaluation.responseRatePercent}}% Response rate
                </strong>
              </li>
            </template>
          </template>
          <template v-else>
            <li class="mb-1">
              Paper-based evaluation
            </li>
            <li class="mb-1">
              <a
                :href="`https://${section.evaluation.domain}.iasystem.org/faculty`"
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
               title="Learn About Course Evaluations"
            ><font-awesome-icon :icon="faQuestionCircle" /></a>
          </li>
          <li v-else class="text-danger">
            <font-awesome-icon :icon="faExclamationTriangle" />
            An error occurred with the course evaluation. Please try again later.
          </li>
        </template>
      </ul>
    </uw-card-property>
  </uw-card-property-group>
</template>

<script>
import {
  faQuestionCircle,
  faExclamationTriangle,
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
    noMarginBottom: {
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