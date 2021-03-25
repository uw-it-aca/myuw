<template>
  <!-- Having myplan courses -->
  <div v-if="hasSections" class="mb-4">
    <div class="d-flex align-items-center mb-2">
      <h3 class="h6 text-dark font-weight-bold flex-fill">
        In MyPlan
      </h3>
      <div class="flex-fill text-right">
        <ul class="list-unstyled m-0">
          <li class="font-weight-bold">
            {{ readyCount }} {{ readyCount == 1 ? "course" : "courses" }} ready
          </li>
          <li class="myuw-text-md">
            <span v-if="unreadyCount">{{ unreadyCount }} not ready</span>
            <b-button
              v-b-toggle="`${summerCardLabel}inMyPlanUnready-collapse-${$meta.uid}`"
              size="sm"
              variant="link"
              class="ml-1 p-0 border-0 bg-transparent align-baseline"
            >
              Plan Details
              <font-awesome-icon v-if="!collapseOpen" :icon="faChevronDown" />
              <font-awesome-icon v-else :icon="faChevronUp" />
            </b-button>
          </li>
        </ul>
      </div>
    </div>
    <b-collapse
      :id="`${summerCardLabel}inMyPlanUnready-collapse-${$meta.uid}`"
      v-model="collapseOpen"
    >
      <div class="bg-light m-0 p-3 border-0 rounded-0">
        <uw-myplan-courses
          :next-term-year="year"
          :next-term-quarter="quarter"
          :my-plan-data="myPlanData"
        />
      </div>
    </b-collapse>
  </div>
  <!-- no myplan courses -->
  <div v-else class="mb-4">
    <div class="d-flex align-items-center mb-2">
      <h3 class="h6 text-dark font-weight-bold flex-fill">
        In MyPlan
      </h3>
      <div class="flex-fill text-right">
        <div class="font-weight-bold">
          No courses in your plan
        </div>
        <div>
          <a
            v-out="'MyPlan Course Search'"
            class="myuw-text-md" target="_blank"
            :href="myplanCourseSearchHref"
          >Add courses</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  faChevronUp,
  faChevronDown,
} from '@fortawesome/free-solid-svg-icons';
import MyplanCoursesComponent from './myplan-courses.vue';

export default {
  components: {
    'uw-myplan-courses': MyplanCoursesComponent,
  },
  props: {
    myPlanData: {
      type: Object,
      required: true,
    },
    year: {
      type: Number,
      required: true,
    },
    quarter: {
      type: String,
      required: true,
    },
    summerCardLabel: {
      type: String,
      default: '',
    },
  },
  data: function() {
    return {
      collapseOpen: false,
      faChevronUp,
      faChevronDown,
    };
  },
  computed: {
    currentPlanData() {
      if (this.myPlanData && this.myPlanData.terms) {
        return this.myPlanData.terms.find(
            (term) => term.quarter.toLowerCase() === this.quarter.toLowerCase(),
        ) || {};
      }
      return {};
    },
    readyCount() {
      return this.currentPlanData.ready_count;
    },
    unreadyCount() {
      return this.currentPlanData.unready_count;
    },
    hasSections() {
      return this.currentPlanData.has_sections;
    },
    myplanCourseSearchHref() {
      return this.currentPlanData.course_search_href;
    },
    courses() {
      return this.currentPlanData.courses;
    },
    coursesUnavailable() {
      return this.courses.filter((c) => !c.registrations_available);
    },
  },
};
</script>

<style lang="scss" scoped>

</style>
