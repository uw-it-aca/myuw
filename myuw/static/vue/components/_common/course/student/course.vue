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
          <uw-collapse :collapseId="`course-details-${index}`">
            <template #collapsed>
              <uw-course-details :section="section"
                display-heading display-instructor class="pt-3" />
            </template>
          </uw-collapse>
        </template>
        <template v-else>
          <uw-collapse :collapseId="`instructors-collapse-${index}`">
            <template #collapsed>
              <uw-instructors
                v-if="section.instructors.length > 0"
                :instructors="section.instructors"
                class="pt-3"
              />
            </template>
          </uw-collapse>
        </template>
      </template>

      <template #card-footer>
        <template
          v-if="section.is_ended || getSectionEval(section.index).length > 0"
        >
          <button
            data-toggle="collapse"
            :data-target="`#course-details-${index}`"
            :aria-controls="`course-details-${index}`"
            aria-expanded="false"
            aria-label="Toggle Course Details"
            type="button"
            class="btn btn-link w-100 p-0 border-0 text-dark"
          >
            Course Details
            <font-awesome-icon v-if="!isOpen" :icon="faChevronDown" class="align-middle" />
            <font-awesome-icon v-else :icon="faChevronUp" class="align-middle" />
          </button>
        </template>

        <template v-else>
          <template v-if="section.instructors.length > 0">
            <button
              data-toggle="collapse"
              :data-target="`#instructors-collapse-${index}`"
              :aria-controls="`instructors-collapse-${index}`"
              aria-expanded="false"
              aria-label="Toggle Course Instructors"
              type="button"
              class="btn btn-link w-100 p-0 border-0 text-dark"
            >
              Instructors
              <font-awesome-icon v-if="!isOpen" :icon="faChevronDown" class="align-middle" />
              <font-awesome-icon v-else :icon="faChevronUp" class="align-middle" />
            </button>
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
import Collapsed from '../../../_templates/collapsed.vue';
import EvalInfo from './course-eval.vue';
import CourseDetails from './course-details.vue';
import Instructors from './instructors.vue';
import CourseHeader from './header.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-collapse': Collapsed,
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
  mounted() {
    const currentUrl = window.location.href;
    if (currentUrl.endsWith(this.section.anchor)) {
      this.selfAnchoredOnce(this.section);
    }
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
