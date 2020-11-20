<template>
  <div>
    <uw-card loaded :ribbon="{ side: 'top', colorId: section.color_id }">
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
            <font-awesome-icon
              :icon="['fas', 'exclamation-triangle']"
              class="mr-1"
            />
            An error has occurred and MyUW cannot display the course evaluation
            information right now. Please try again later.
          </p>
        </template>

        <uw-course-details
          v-else-if="!section.is_ended"
          :course="course"
          :section="section"
        />
      </template>

      <template #card-disclosure>
        <template
          v-if="section.is_ended || getSectionEval(section.index).length > 0"
        >
          <b-collapse :id="`course-details-${index}`" v-model="isOpen">
            <!-- creates line spacer above meeting info -->
            <div class="d-flex">
              <div class="w-25">
                &nbsp;
              </div>
              <div class="w-75">
                <hr>
              </div>
            </div>
            <uw-course-details
              :course="course"
              :section="section"
            />
          </b-collapse>
        </template>
        <template v-else>
          <b-collapse :id="`instructors-collapse-${index}`" v-model="isOpen">
            <!-- creates line spacer above instructor info -->
            <div class="d-flex">
              <div class="w-25">
                &nbsp;
              </div>
              <div class="w-75">
                <hr>
              </div>
            </div>
            <uw-instructors
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
          <template v-if="section.instructors.length > 0">
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
          </template>
          <div v-else class="text-center text-muted font-italic myuw-text-md"
               style="line-height:1.5rem"
          >
            No instructor information available
          </div>
        </template>
      </template>
    </uw-card>
  </div>
</template>

<script>
import {mapGetters, mapState} from 'vuex';
import Card from '../../../_templates/card.vue';
import EvalInfo from './course-eval.vue';
import CourseDetails from './course-details.vue';
import Instructors from './instructors.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-course-details': CourseDetails,
    'uw-course-eval': EvalInfo,
    'uw-instructors': Instructors,
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
