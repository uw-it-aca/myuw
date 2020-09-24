<template>
  <div v-if="courses">
    <h4>In MyPlan</h4>
    <div>
      <ul>
        <li>{{readyCount}} {{readyCount > 1 ? "courses" : "course"}} ready</li>
        <li v-if="unreadyCount">
          {{unreadyCount}} not ready
          <a v-if="hasSections" target="_blank" :href="myplanHref">
            Add Sections
          </a>
          <button
            v-else v-b-toggle="`${summerCardLabel}inMyPlanUnready-collapse`"
            title="Expand to show courses not ready"
          >
            {{collapseOpen ? "Hide Details" : "See Details"}}
          </button>
        </li>
      </ul>
    </div>
    <b-collapse :id="`${summerCardLabel}inMyPlanUnready-collapse`">
      <h4>Not ready for registration</h4>
      <ul>
        <li v-for="(course, i) in coursesUnavailable" :key="i">
          {{course.curriculum_abbr}} {{course.course_number}}
        </li>
      </ul>

      <div>
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

      <div>
        <a
          title="Edit plan to fix issues" target="_blank"
          :href="myplanHref"
        >
          Edit plan in MyPlan
        </a>
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
import {mapGetters, mapState, mapActions} from 'vuex';

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
      default: "",
    },
  },
  data: function() {
    return {
      collapseOpen: false,
    }
  },
  computed: {
    currentPlanData() {
      return this.myPlanData.terms.find(
        (term) => term.quarter === this.quarter
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
    }
  },
}
</script>

<style lang="scss" scoped>

</style>