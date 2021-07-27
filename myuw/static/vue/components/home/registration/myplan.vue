<template>
  <!-- Having myplan courses -->
  <div v-if="hasSections || hasUnreadyCourses" class="mb-4">

    <uw-card-status>
      <template #status-label>In MyPlan</template>
      <template #status-value>
        <ul class="list-unstyled m-0">
          <li class="font-weight-bold">
            {{ readyCount }} {{ readyCount == 1 ? "course" : "courses" }} ready
          </li>
        </ul>
      </template>
      <template #status-content>
        <div class="d-flex mb-2 myuw-text-md">
          <div class="flex-fill w-50"></div>
          <div class="flex-fill w-50 text-right">
            <ul class="list-unstyled m-0">
              <li class="myuw-text-md">
                <span v-if="hasUnreadyCourses">{{ unreadyCount }} not ready</span>
                <button v-b-toggle="`${summerCardLabel}inMyPlanUnready-collapse-${$meta.uid}`"
                  type="button"
                  class="btn btn-link btn-sm ml-1 p-0 border-0 bg-transparent align-baseline"
                >
                  Plan Details
                  <font-awesome-icon v-if="!collapseOpen" :icon="faChevronDown" />
                  <font-awesome-icon v-else :icon="faChevronUp" />
                </button>
              </li>
            </ul>
          </div>
        </div>
      </template>
    </uw-card-status>
    <div :id="`${summerCardLabel}inMyPlanUnready-collapse-${$meta.uid}`"
      v-model="collapseOpen"
      class="collapse"
    >
      <div class="bg-light m-0 p-3 border-0 rounded-0">
        <uw-myplan-courses
          :next-term-year="year"
          :next-term-quarter="quarter"
          :my-plan-data="myPlanData"
        />
      </div>
    </div>
  </div>

  <!-- no myplan courses -->
  <div v-else class="mb-4">
    <uw-card-status>
      <template #status-label>In MyPlan</template>
      <template #status-value>
        No courses in your plan
      </template>
      <template #status-content>
        <div class="d-flex mb-2 myuw-text-md">
          <div class="flex-fill w-50"></div>
          <div class="flex-fill w-50 text-right">
            <a
              v-out="'MyPlan Course Search'"
              class="myuw-text-md"
              :href="myplanCourseSearchHref"
            >Add courses</a>
          </div>
        </div>
      </template>
    </uw-card-status>
  </div>
</template>

<script>
import CardStatus from '../../_templates/card-status.vue';
import {
  faChevronUp,
  faChevronDown,
} from '@fortawesome/free-solid-svg-icons';
import MyplanCoursesComponent from './myplan-courses.vue';

export default {
  components: {
    'uw-card-status': CardStatus,
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
    hasUnreadyCourses() {
      return this.currentPlanData.has_unready_courses;
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
