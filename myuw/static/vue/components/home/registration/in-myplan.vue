<template>
  <div v-if="courses" class="mb-4">
    <div class="d-flex align-items-center mb-2">
      <h4 class="h6 text-dark font-weight-bold flex-fill">
        In MyPlan
      </h4>
      <div class="flex-fill text-right">
        <ul class="list-unstyled m-0">
          <li class="font-weight-bold">
            {{ readyCount }}
            {{ readyCount > 1 ? "courses" : "course" }}
            ready
          </li>
          <li v-if="unreadyCount" class="myuw-text-sm">
            {{ unreadyCount }} not ready
            <b-button
              v-b-toggle="`${summerCardLabel}inMyPlanUnready-collapse-${_uid}`"
              :title="buttonTitle"
              size="sm"
              variant="link"
              class="p-0 border-0 bg-transparent align-baseline"
            >
              {{ collapseOpen ? "Hide Details" : "See Details" }}
            </b-button>
          </li>
        </ul>
      </div>
    </div>
    <b-collapse
      :id="`${summerCardLabel}inMyPlanUnready-collapse-${_uid}`"
      v-model="collapseOpen"
    >
      <div class="bg-light m-0 p-3 border-0 rounded-0">
        <h5>Your TERM YEAR Plan</h5>
        <h6 class="font-weight-bold">
          Issues
        </h6>
        <p class="myuw-text-md">
          The following plan items have issues you must resolve before they
          can be sent to Registration:
        </p>

        <ul class="list-unstyled myuw-text-sm">
          <li v-for="(course, i) in coursesUnavailable" :key="i">
            {{ course.curriculum_abbr }} {{ course.course_number }}
          </li>
        </ul>

        <div class="text-right myuw-text-sm">
          <a
            title="Edit plan to fix issues" target="_blank"
            :href="myplanHref"
          >
            Go to your TERM YEAR plan to resolve these issues
          </a>
        </div>

        <h6 class="font-weight-bold">
          Ready for registration
        </h6>
        <div class="text-danger">
          TODO: myplan table from footer collapse goes here
        </div>
      </div>
    </b-collapse>
  </div>
  <div v-else>
    <h4>In MyPlan</h4>
    <div>No courses in your plan</div>
    <div>
      <a target="_blank" :href="myplanCourseSearchHref">
        Add courses
      </a>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    myPlanData: {
      type: Object,
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
    };
  },
  computed: {
    currentPlanData() {
      if (this.myPlanData && this.myPlanData.terms) {
        return this.myPlanData.terms.find(
            (term) => term.quarter === this.quarter,
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
    myplanHref() {
      return this.currentPlanData.myplan_href;
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
    buttonTitle() {
      if (this.collapseOpen) return 'Collapse to hide courses not ready';
      return 'Expand to show courses not read';
    },
  },
};
</script>

<style lang="scss" scoped>

</style>
