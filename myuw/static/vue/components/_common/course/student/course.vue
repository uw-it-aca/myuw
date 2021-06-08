<template>
  <div v-meta="{term: term, course: section.anchor}">
    <uw-card
      :id="section.anchor"
      loaded
      :ribbon="{ side: 'top', colorId: section.color_id }"
    >
      <template #card-heading>
        <uw-course-header :section="section" />
      </template>

      <template #card-body>
        <uw-course-eval
          v-if="isReadyEval && getSectionEval(section.index).length > 0"
          :eval-data="getSectionEval(section.index)"
          :section="section"
        />
        <template v-else-if="isErroredEval && statusCodeEvals != 404" loaded>
          <p>
            <font-awesome-icon :icon="faExclamationTriangle" class="mr-1" />
            An error has occurred and MyUW cannot display the course evaluation
            information right now. Please try again later.
          </p>
        </template>

        <uw-course-details v-else-if="!section.is_ended" :section="section"/>
      </template>

      <template #card-disclosure>
        <template
          v-if="section.is_ended || getSectionEval(section.index).length > 0"
        >
          <b-collapse
            :id="`course-details-${index}`"
            v-model="isOpen"
          >
            <uw-course-details :section="section"
              displayHeading=true displayInstructor=true class="pt-3"/>
          </b-collapse>
        </template>
        <template v-else>
          <b-collapse
            :id="`instructors-collapse-${index}`"
            v-model="isOpen"
          >
            <uw-instructors
              v-if="section.instructors.length > 0"
              :instructors="section.instructors"
              class="pt-3"
            />
          </b-collapse>
        </template>
      </template>

      <template #card-footer>
        <template
          v-if="section.is_ended || getSectionEval(section.index).length > 0"
        >
          <b-button
            v-b-toggle="`course-details-${index}`"
            variant="link"
            size="sm"
            class="w-100 p-0 border-0 text-dark"
          >
            Course Details
            <font-awesome-icon v-if="!isOpen" :icon="faChevronDown" class="align-middle" />
            <font-awesome-icon v-else :icon="faChevronUp" class="align-middle" />
          </b-button>
        </template>

        <template v-else>
          <template v-if="section.instructors.length > 0">
            <b-button
              v-b-toggle="`instructors-collapse-${index}`"
              variant="link"
              size="sm"
              class="w-100 p-0 border-0 text-dark"
            >
              Instructors
              <font-awesome-icon v-if="!isOpen" :icon="faChevronDown" class="align-middle" />
              <font-awesome-icon v-else :icon="faChevronUp" class="align-middle" />
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
import {
  faChevronUp,
  faChevronDown,
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';
import {mapGetters, mapState} from 'vuex';
import Card from '../../../_templates/card.vue';
import EvalInfo from './course-eval.vue';
import CourseDetails from './course-details.vue';
import Instructors from './instructors.vue';
import CourseHeader from './header.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-course-details': CourseDetails,
    'uw-course-eval': EvalInfo,
    'uw-instructors': Instructors,
    'uw-course-header': CourseHeader,
  },
  props: {
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
      faChevronUp,
      faChevronDown,
      faExclamationTriangle,
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
    term() {
      return this.section.year + "," + this.section.quarter;
    },
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
  mounted() {
    const currentUrl = window.location.href;
    if (currentUrl.endsWith(this.section.anchor)) {
      this.selfAnchoredOnce(this.section);
    }
  },
};
</script>
