<template>
  <div>
    <div :class="`w-100 myuw-border-top border-c${section.color_id}`" />
    <uw-card loaded>
      <template #card-heading>
        <div class="d-flex justify-content-between mb-3">
          <div>
            <h4 class="h5 mb-0 text-dark-beige myuw-font-encode-sans">
              {{ section.curriculum_abbr }}
              {{ section.course_number }}
              {{ section.section_id }}
            </h4>
            <div>{{ section.course_title }}</div>
          </div>
          <div>
            <div :class="`px-1 border myuw-text-sm
            text-uppercase text-c${section.color_id}`"
            >
              {{ ucfirst(section.section_type) }}
            </div>
            <div
              v-if="section.is_primary_section && section.for_credit"
              :class="`px-1 myuw-text-sm text-right
              text-uppercase text-c${section.color_id}`"
            >
              {{ section.credits }} CR
            </div>
          </div>
        </div>
      </template>

      <template #card-body>
        <uw-course-eval
          v-if="isReadyEval && getSectionEval(section.index).length > 0"
          :eval-data="getSectionEval(section.index)"
          :section="section"
        />
        <template v-else-if="isErroredEval && statusCodeEvals != 404" loaded>
          <p>
            <i class="fa fa-exclamation-triangle" />
            An error has occurred and MyUW cannot display the course evaluation
            information right now. Please try again later.
          </p>
        </template>

        <uw-course-details
          v-else-if="!section.is_ended"
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
