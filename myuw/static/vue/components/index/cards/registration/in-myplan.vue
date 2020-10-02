<template>
  <div v-if="courses">
    <div class="d-flex align-items-center mb-2">
      <h4 class="h6 text-dark flex-fill">
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
            <a v-if="!hasSections" target="_blank" :href="myplanHref">
              Add Sections
            </a>
            <b-button
              v-else v-b-toggle="`${summerCardLabel}inMyPlanUnready-collapse`"
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
      :id="`${summerCardLabel}inMyPlanUnready-collapse`"
      v-model="collapseOpen"
    >
      <div class="bg-light m-0 p-3 border-0 rounded-0">
        <h5 class="h6 font-weight-bold">
          Not ready for registration
        </h5>
        <ul class="myuw-text-md">
          <li v-for="(course, i) in coursesUnavailable" :key="i">
            {{ course.curriculum_abbr }} {{ course.course_number }}
          </li>
        </ul>

        <div class="myuw-text-md">
          <p>
            One or more of the issues below will prevent these courses from
            being sent to registration:
          </p>
          <ul>
            <li>Too many/too few sections selected for a course</li>
            <li>Time conflict with registered course</li>
            <li>Time conflict with a selected section</li>
            <li>Planned courses are jointly offered versions of one course</li>
          </ul>
        </div>
        <div class="text-right myuw-text-md">
          <a
            title="Edit plan to fix issues" target="_blank"
            :href="myplanHref"
          >
            Edit plan in MyPlan
          </a>
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
      return this.myPlanData.terms.find(
          (term) => term.quarter === this.quarter,
      );
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
