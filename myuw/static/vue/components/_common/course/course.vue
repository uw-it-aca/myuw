<template>
  <div>
    <div :class="`w-100 myuw-border-top border-c${section.color_id}`" />
    <uw-card loaded>
      <template #card-heading>
        <div class="d-flex justify-content-between">
          <div>
            <h4>
              {{ section.curriculum_abbr }}
              {{ section.course_number }}
              {{ section.section_id }}
            </h4>
            <span>{{ section.course_title }}</span>
          </div>
          <div>
            <span class="d-block">
              {{ ucfirst(section.section_type) }}
            </span>
            <span
              v-if="section.is_primary_section && section.for_credit"
              class="d-block text-right"
            >
              {{ section.credits }} CR
            </span>
          </div>
        </div>
        <div v-if="section.summer_term">
          Summer {{ section.summer_term.split('-').map(ucfirst).join('-') }}
        </div>
        <div v-if="section.cc_display_dates">
          Dates: {{ sectionFormattedDates(section) }}
        </div>
        <div v-if="section.on_standby">
          Your status: On Standby
        </div>
      </template>

      <template #card-body>
        <uw-course-eval
          v-if="isReadyEval"
          :eval-data="getSectionEval(section.index)"
          :section="section"
        />
        <template v-else-if="isErroredEval && statusCodeEvals != 404" loaded>
          <p>
            <i class="fa fa-exclamation-triangle" aria-hidden="true"></i>
            An error has occurred and MyUW cannot display the course evaluation
            information right now. Please try again later.
          </p>
        </template>
        <uw-course-details
          v-if="!section.is_ended"
          :course="course"
          :section="section"
          :show-row-heading="showRowHeading "
        />
      </template>

      <template #card-disclosure>
        <template
          v-if="section.is_ended || getSectionEval(section.index).length > 0"
        >
          <b-collapse :id="`course-details-${index}`" v-model="isOpen">
            <uw-course-details
              :course="course"
              :section="section"
              :show-row-heading="showRowHeading "
            />
          </b-collapse>
        </template>
        <template v-else>
          <b-collapse :id="`instructors-collapse-${index}`" v-model="isOpen">
            <uw-instructor-info
              v-if="section.instructors.length > 0"
              :instructors="section.instructors"
            />
          </b-collapse>
        </template>
      </template>

      <template #card-footer>
        <template
          v-if="section.is_ended || getSectionEval(section.index).length > 0"
        >
          <b-button
            v-if="!isOpen"
            v-b-toggle="`course-details-${index}`"
            variant="link"
            size="sm"
            class="w-100 p-0 border-0 text-dark"
            aria-label="SHOW COURSE DETAILS"
            title="Expand to show course details"
          >
            SHOW COURSE DETAILS
          </b-button>
          <b-button
            v-else
            v-b-toggle="`course-details-${index}`"
            variant="link"
            size="sm"
            class="w-100 p-0 border-0 text-dark"
            aria-label="HIDE COURSE DETAILS"
            title="Collapse to hide course details"
          >
            HIDE COURSE DETAILS
          </b-button>
        </template>

        <template v-else>
          <span v-if="section.instructors.length > 0">
            <b-button
              v-if="!isOpen"
              v-b-toggle="`instructors-collapse-${index}`"
              variant="link"
              size="sm"
              class="w-100 p-0 border-0 text-dark"
              aria-label="SHOW INSTRUCTORS"
              title="Expand to show instructors"
            >
              SHOW INSTRUCTORS
            </b-button>
            <b-button
              v-else
              v-b-toggle="`instructors-collapse-${index}`"
              variant="link"
              size="sm"
              class="w-100 p-0 border-0 text-dark"
              aria-label="HIDE INSTRUCTORS"
              title="Collapse to hide instructors"
            >
              HIDE INSTRUCTORS
            </b-button>
          </span>
          <span v-else>
            No instructor information available
          </span>
        </template>
      </template>
    </uw-card>
  </div>
</template>

<script>
import {mapGetters, mapState} from 'vuex';
import dayjs from 'dayjs';
import Card from '../../_templates/card.vue';
import EvalInfo from './course-eval.vue';
import CourseDetails from './course-details.vue';
import InstructorInfo from './instructor-info.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-course-details': CourseDetails,
    'uw-course-eval': EvalInfo,
    'uw-instructor-info': InstructorInfo,
  },
  props: {
    course: {
      type: Object,
      required: true,
    },
    section: {
      type: Object,
      required: true,
    },
    showRowHeading: {
      type: Boolean,
      default: false,
    },
    index: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      isOpen: false,
    };
  },
  computed: {
    ...mapState('iasystem', {
      evalData(state) {
        return state.value;
      },
    }),
    ...mapGetters('iasystem', {
      isReadyEval: 'isReady',
      isErroredEval: 'isErrored',
      statusCodeEvals: 'statusCode',
    }),
  },
  methods: {
    sectionFormattedDates(section) {
      return `${
        dayjs(section.start_date).format('MMM D')
      } - ${dayjs(section.end_date).format('MMM D')}`;
    },
    getSectionEval(index) {
      if (
        this.evalData &&
        this.evalData.sections &&
        this.evalData.sections[index]
      ) {
        return this.evalData.sections[index].evaluation_data || [];
      }
      return [];
    },
  },
};
</script>
