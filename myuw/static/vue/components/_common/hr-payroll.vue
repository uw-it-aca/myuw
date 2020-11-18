<template>
  <uw-card v-if="showCard" :loaded="true">
    <template #card-heading>
      <h3>
        HR and Payroll
      </h3>
    </template>
    <template #card-body>
      <div style="position:relative;">
        <h4 class="sr-only">
          Workday
        </h4>
        <div>
          <a id="og_workday" class="myuw-workday-btn myuw-btn btn btn-default" href="https://wd5.myworkday.com/uw/login.htmld" data-linklabel="Workday" :style="workdayIconStyle">
            Sign in to Workday
          </a>
        </div>
        <p>
          Workday is the University’s cloud-based
          HR/payroll operations system.
        </p>
        <p>
          *Please note: The Medical Centers continue
          to use Kronos for time-tracking and payroll.
        </p>
      </div>
      <div v-if="!studentEmployee">
        <h4>Get Help</h4>
        <ul class="unstyled-list">
          <li>
            <a v-if="faculty" href="https://ap.washington.edu/ahr/" target="_blank">Academic HR</a>
            <a v-else href="https://hr.uw.edu/">UW Human Resources</a>
          </li>
          <li>
            <a href="https://isc.uw.edu/" target="_blank">Integrated Service Center (ISC)</a>
            <p v-if="!truncateView" class="myuw-text-small">
              Learn how to <a href="https://isc.uw.edu/your-time-absence/time-off/" data-linklabel="ISC Time Off" target="_blank">look up sick and vacation time</a>, <a href="https://isc.uw.edu/your-time-absence/time-reporting/" target="_blank" data-linklabel="ISC Time Reporting">report time worked</a>, <a href="https://isc.uw.edu/user-guides/edit_personal_information/" data-linklabel="ISC Edit Personal Address" target="_blank">update personal information</a>, and more.
            </p>
          </li>
        </ul>
      </div>
      <div v-else>
        <h4>Related</h4>
        <ul class="unstyled-list">
          <li><a href="https://hr.uw.edu/" target="_blank">UW Human Resources</a></li>
          <li><a href="https://hr.uw.edu/benefits/insurance/health/graduate-appointees/" target="_blank">Graduate Appointee Insurance Program (GAIP)</a></li>
          <li><a href="https://grad.uw.edu/graduate-student-funding/funding-information-for-departments/administering-assistantships/ta-ra-salaries/" target="_blank">Teaching or research assistant salary schedules</a></li>
          <li>
            <a href="https://isc.uw.edu/" target="_blank">Integrated Service Center (ISC)</a>
            <p>
              Learn how to <a href="https://isc.uw.edu/your-time-absence/time-reporting/" data-linklabel="ISC Enter Time" target="_blank">enter your hours in Workday</a>, <a href="https://isc.uw.edu/your-pay-taxes/paycheck-info/#direct-deposit" target="_blank" data-linklabel="ISC Set Up direct deposit">set up direct deposit</a>, and more.
            </p>
          </li>
        </ul>
      </div>
    </template>
  </uw-card>
</template>

<script>
import {mapState} from 'vuex';
import Card from '../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  props: {
    isHomePage: {
      type: Boolean,
      default: false,
    },
    isAccountsPage: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapState({
      showCard: function(state) {
        if (this.isHomePage &&
          state.user.affiliations.employee &&
          !state.user.affiliations.student &&
          !state.user.affiliations.instructor ||
          state.user.affiliations.retiree ||
          state.user.affiliations.past_employee) {
          return true;
        } else if (this.isAccountsPage &&
               state.user.affiliations.stud_employee ||
               state.user.affiliations.instructor) {
          return true;
        } else {
          return false;
        }
      },
      workdayIconStyle: (state) => 'background-image: url(\'' + state.staticUrl + 'images/wday_logo.png\';',
      truncateView: (state) => (state.user.affiliations.retiree ||
                                state.user.affiliations.past_employee),
      studentEmployee: (state) => state.user.affiliations.stud_employee,
      faculty: (state) => state.user.affiliations.faculty,
    }),
  },
};
</script>

<style lang="scss" scoped>
</style>
