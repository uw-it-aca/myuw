<template>
  <uw-card v-if="showOutageCard" :loaded="true" class="myuw-outage">
    <template #card-heading>
      <h2 class="h4 mb-3 text-danger myuw-font-encode-sans">
        Limited data due to technical difficulties
      </h2>
    </template>
    <template #card-body>
      <!-- custom error message for outages -->
      <div
        class="alert alert-light p-0 border-0 bg-transparent"
        role="alert"
      >
        <div class="d-flex text-danger m-0 myuw-text-md">
          <div class="pe-2 flex-shrink-1">
            <font-awesome-icon :icon="faExclamationTriangle" />
          </div>
          <div class="w-100">
            We are aware of the issue and working on it. Please try again later.
          </div>
        </div>
      </div>

      <h3 class="h6 text-dark-beige myuw-font-encode-sans">
        Things you might be looking for:
      </h3>

      <ul class="list-unstyled myuw-text-md">
        <li v-if="isInstructor || isStudent" class="mb-1">
          <a href="https://canvas.uw.edu/">Canvas LMS</a>
        </li>
        <li v-if="isInstructor || isStudent" class="mb-1">
          <a href="https://catalyst.uw.edu/">Catalyst Web Tools</a>
        </li>
        <li v-if="isStudent" class="mb-1">
          <a href="https://sdb.admin.uw.edu/students/uwnetid/register.asp"
          >Student Registration</a>
        </li>
        <li v-if="isStudent" class="mb-1">
          <a href="https://sdb.admin.uw.edu/students/uwnetid/schedule.asp"
          >Student Class Schedule</a>
        </li>
        <li v-if="isStudent" class="mb-1">
          <a href="https://sdb.admin.uw.edu/sisStudents/uwnetid/tuition.aspx"
          >Student Tuition Statement</a>
        </li>
        <li v-if="isInstructor || isStudent" class="mb-1">
          <a href="https://www.washington.edu/students/timeschd/"
          >Time Schedule</a>
        </li>
        <li v-if="isStudent" class="mb-1">
          <a href="https://myplan.uw.edu"
          >MyPlan</a>
        </li>
        <li v-if="isInstructor" class="mb-1">
          <a href="https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/default.aspx"
          >My Class Instructor Resources</a>
        </li>
        <li v-if="isInstructor" class="mb-1">
          <a href="https://gradepage.uw.edu/">GradePage</a>
        </li>
        <li class="mb-1">
          <a href="https://uw.hosted.panopto.com/">Panopto Lecture Capture</a>
        </li>
        <li class="mb-1">
          <a href="https://eo.admin.washington.edu/uweomyuw/outage/uwnetid/myuwoutage.asp"
          >UW Professional &amp; Continuing Education</a>
        </li>
        <li v-if="isEmployee && !isAcademicsPage" class="mb-1">
          <a href="https://wd5.myworkday.com/uw/d/home.htmld"
          >Workday</a>
        </li>
        <li v-if="isEmployee && !isAcademicsPage" class="mb-1">
          <a href="http://ucs.admin.uw.edu/myfd/"
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
    isAcademicsPage: {
      type: Boolean,
      default: false,
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
      isEmployee: (state) => state.user.affiliations.all_employee,
    }),
    ...mapGetters('inst_schedule', {
      instScheduleErrored: 'isErroredTagged',
      instScheduleStatusCode: 'statusCodeTagged',
    }),
    ...mapGetters('stud_schedule', {
      studScheduleErrored: 'isErroredTagged',
      studScheduleStatusCode: 'statusCodeTagged',
    }),
    ...mapGetters('notices', {
      noticeErrored: 'isErrored',
      noticeStatusCode: 'statusCode',
    }),
    ...mapGetters('profile', {
      studProfileErrored: 'isErrored',
      studProfileStatusCode: 'statusCode',
    }),
    ...mapGetters('directory', {
      empProfileErrored: 'isErrored',
      empProfileStatusCode: 'statusCode',
    }),
    noticeDataError() {
      return this.noticeErrored && this.noticeStatusCode !== 404;
    },
    scheDataError() {
      return this.studScheduleErrored(this.term) &&
        this.studScheduleStatusCode(this.term) !== 404;
    },
    studProfileDataError() {
        return this.studProfileErrored && this.studProfileStatusCode !== 404;
    },
    studDataError() {
      return this.isStudent &&
        (this.noticeDataError || this.scheDataError || this.studProfileDataError);
    },
    instDataError() {
      return this.isInstructor &&
        this.instScheduleErrored(this.term) &&
        this.instScheduleStatusCode(this.term) !== 404;
    },
    employeeDataError() {
      return this.isEmployee && this.empProfileErrored &&
        this.empProfileStatusCode !== 404;
    },
    showOutageCard() {
      return (this.isAcademicsPage ? this.studDataError :
        this.studDataError || this.instDataError || this.employeeDataError);
    },
  },
  created() {
    if (this.isStudent) {
      this.fetchNotices();
      this.fetchSchedule(this.term);
      this.fetchProfile();
    }
    if (!this.isAcademicsPage && this.isInstructor) {
      this.fetchInstSchedule(this.term);
    }
    if (!this.isAcademicsPage && this.isEmployee) {
      this.fetchEmployeeProfile();
    }
  },
  methods: {
    ...mapActions('notices', {
      fetchNotices: 'fetch',
    }),
    ...mapActions('stud_schedule', {
      fetchSchedule: 'fetch',
    }),
    ...mapActions('profile', {
      fetchProfile: 'fetch',
    }),
    ...mapActions('inst_schedule', {
      fetchInstSchedule: 'fetch',
    }),
    ...mapActions('directory', {
      fetchEmployeeProfile: 'fetch',
    }),
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import '../../../css/myuw/variables.scss';

.myuw-outage {
  // override card background color using new warning theme background
  ::v-deep .card-body {
    background-color: lighten(
      map.get($theme-colors, 'warning'), 49%
    ) !important;
  }


}
</style>
