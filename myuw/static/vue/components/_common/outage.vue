<template>
  <uw-card v-if="showOutageCard" :loaded="true" class="myuw-outage">
    <template #card-heading>
      <h2 class="text-danger">
        Limited data due to technical difficulties
      </h2>
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

      <h3 class="h6 font-weight-bold">
        Things you might be looking for:
      </h3>

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
      return this.studDataError || this.instDataError || this.employeeDataError;
    },
  },
  created() {
    if (this.isStudent) {
      this.fetchNotices();
      this.fetchSchedule(this.term);
      this.fetchProfile();
    }
    if (this.isInstructor) {
      this.fetchInstSchedule(this.term);
    }
    if (this.isEmployee) {
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
  ::v-deep .card {
    background-color: lighten(
      map.get($theme-colors, 'warning'), 49%
    ) !important;
  }
}
</style>
