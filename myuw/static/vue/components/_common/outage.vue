<template>
  <uw-card v-if="showOutageCard" :loaded="true" class="myuw-outage">
    <template #card-heading>
      <h3 class="text-danger">
        Limited data due to technical difficulties
      </h3>
    </template>
    <template #card-body>
      <!-- custom error message for outages -->
      <b-alert show variant="light" class="p-0 border-0 bg-transparent">
        <div class="d-flex text-danger m-0 myuw-text-md">
          <div class="pr-2 flex-shrink-1">
            <font-awesome-icon :icon="faExclamationTriangle" />
          </div>
          <div class="w-100">
            We are aware of the issue and working on it. Please try again later.
          </div>
        </div>
      </b-alert>

      <h4 class="h6 font-weight-bold">
        Things you might be looking for:
      </h4>

      <ul class="list-unstyled myuw-text-md">
        <li class="mb-1">
          <a href="https://canvas.uw.edu/" target="_blank">Canvas LMS</a>
        </li>
        <li class="mb-1">
          <a href="https://catalyst.uw.edu/" target="_blank">Catalyst Web Tools</a>
        </li>
        <li class="mb-1">
          <a href="https://sdb.admin.uw.edu/students/uwnetid/register.asp"
             target="_blank"
          >Student Registration</a>
        </li>
        <li class="mb-1">
          <a href="https://sdb.admin.uw.edu/students/uwnetid/schedule.asp"
             target="_blank"
          >Student Class Schedule</a>
        </li>
        <li class="mb-1">
          <a href="https://sdb.admin.uw.edu/sisStudents/uwnetid/tuition.aspx"
             target="_blank"
          >Student Tuition Statement</a>
        </li>
        <li class="mb-1">
          <a href="https://www.washington.edu/students/timeschd/"
             target="_blank"
          >Time Schedule</a>
        </li>
        <li class="mb-1">
          <a href="https://myplan.uw.edu"
             target="_blank"
          >MyPlan</a>
        </li>
        <li class="mb-1">
          <a href="https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/default.aspx"
             target="_blank"
          >My Class Instructor Resources</a>
        </li>
        <li class="mb-1">
          <a href="https://gradepage.uw.edu/" target="_blank">GradePage</a>
        </li>
        <li class="mb-1">
          <a href="https://uw.hosted.panopto.com/" target="_blank">Panopto Lecture Capture</a>
        </li>
        <li class="mb-1">
          <a href="https://eo.admin.washington.edu/uweomyuw/outage/uwnetid/myuwoutage.asp"
             target="_blank"
          >UW Professional &amp; Continuing Education</a>
        </li>
        <li class="mb-1">
          <a href="https://wd5.myworkday.com/uw/d/home.htmld"
             target="_blank"
          >Workday</a>
        </li>
        <li class="mb-1">
          <a href="http://ucs.admin.uw.edu/myfd/"
             target="_blank"
          >MyFinancial.desktop</a>
        </li>
      </ul>
    </template>
  </uw-card>
</template>

<script>
import {
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';
import {mapGetters, mapActions, mapState} from 'vuex';
import Card from '../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  props: {
    term: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      faExclamationTriangle,
    };
  },
  computed: {
    ...mapState({
      isStudent: (state) => state.user.affiliations.student,
      isInstructor: (state) => state.user.affiliations.instructor,
      isEmployee: (state) => state.user.affiliations.employee,
    }),
    ...mapGetters({
      studentScheduleStatusCode: 'stud_schedule/statusCodeTagged',
      noticeStatusCode: 'notices/statusCode',
      profileStatusCode: 'profile/statusCode',
      /** These modules don't exist yet.
       * Commenting them for later implementation.
       * TODO: Implement the profile, instructorSchedule,
       * and directory api calls.
      instructorScheduleStatusCode: 'instructorSchedule/statusCode',
      directoryStatusCode: 'directory/statusCode',
      */
    }),
    showOutageCard: function() {
      if (this.isStudent) {
        return this.non404Error(this.studentScheduleStatusCode(this.term)) ||
            this.non404Error(this.noticeStatusCode) ||
            this.non404Error(this.profileStatusCode);
      }
      /** This is the logic for instructor and employee
      if (this.isInstructor) {
        if (this.instructorScheduleStatusCode) {
          if (this.non404Error(this.instructorScheduleStatusCode)) {
            return true;
          }
        }
      }

      if (this.isEmployee) {
        if (this.directoryStatusCode) {
          if (this.non404Error(this.directoryStatusCode)) {
            return true;
          }
        }
      }
      */
      return false;
    },
  },
  created() {
    if (this.isStudent) {
      this.fetchSchedule(this.term);
      this.fetchProfile();
      this.fetchNotices();
    }

    if (this.isInstructor) {
      // Fetch instructor data
    }

    if (this.isEmployee) {
      // Fetch employee data
    }
  },
  methods: {
    // Client errors (400–499)
    // and Server errors (500–599).
    non404Error(statusCode) {
      // The status codes could be undefined before page is loaded.
      if (!statusCode) {
        return false;
      }
      return (statusCode < 600 && statusCode >= 400 && statusCode !== 404);
    },
    ...mapActions('notices', {
      fetchNotices: 'fetch',
    }),
    ...mapActions('stud_schedule', {
      fetchSchedule: 'fetch',
    }),
    ...mapActions('profile', {
      fetchProfile: 'fetch',
    }),
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import '../../../css/myuw/variables.scss';

.myuw-outage {
  // override card background color using new warning theme background
  ::v-deep .card {
    background-color: lighten(
      map.get($theme-colors, 'warning'), 49%
    ) !important;
  }
}
</style>
