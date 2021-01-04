<template>
  <uw-card v-if="showCard" :loaded="true">
    <template #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">HR and Payroll</h3>
    </template>
    <template #card-body>
      <div style="position: relative">
        <h4 class="sr-only">Workday</h4>
        <p>
          <a
            id="og_workday"
            class="btn btn-outline-beige text-dark myuw-text-md out-link myuw-workday"
            href="https://wd5.myworkday.com/uw/login.htmld"
            target="_blank"
            data-linklabel="Workday"
            :style="`background-image: url(${staticUrl}images/wday_logo.png);`"
          >
            Sign in to Workday
          </a>
        </p>
        <p class="myuw-text-sm">
          Workday is the University’s cloud-based HR/payroll operations system.
        </p>
        <p class="myuw-text-sm">
          *Please note: The Medical Centers continue to use Kronos for time-tracking and payroll.
        </p>
      </div>
      <div v-if="!studEmployee">
        <h4 class="h6 font-weight-bold text-dark-beige">Get Help</h4>
        <ul class="list-unstyled myuw-text-md">
          <li>
            <a v-if="faculty" href="https://ap.washington.edu/ahr/" target="_blank">Academic HR</a>
            <a v-else href="https://hr.uw.edu/">UW Human Resources</a>
          </li>
          <li>
            <a href="https://isc.uw.edu/" target="_blank">Integrated Service Center (ISC)</a>
            <div v-if="!truncateView" class="myuw-text-sm text-muted">
              Learn how to
              <a
                href="https://isc.uw.edu/your-time-absence/time-off/"
                data-linklabel="ISC Time Off"
                target="_blank"
                >look up sick and vacation time</a
              >,
              <a
                href="https://isc.uw.edu/your-time-absence/time-reporting/"
                target="_blank"
                data-linklabel="ISC Time Reporting"
                >report time worked</a
              >,
              <a
                href="https://isc.uw.edu/user-guides/edit_personal_information/"
                data-linklabel="ISC Edit Personal Address"
                target="_blank"
                >update personal information</a
              >, and more.
            </div>
          </li>
        </ul>
      </div>
      <div v-else>
        <h4 class="h6 font-weight-bold text-dark-beige">Related</h4>
        <ul class="list-unstyled myuw-text-md">
          <li><a href="https://hr.uw.edu/" target="_blank">UW Human Resources</a></li>
          <li>
            <a
              href="https://hr.uw.edu/benefits/insurance/health/graduate-appointees/"
              target="_blank"
              >Graduate Appointee Insurance Program (GAIP)</a
            >
          </li>
          <li>
            <a
              href="https://grad.uw.edu/graduate-student-funding/funding-information-for-departments/administering-assistantships/ta-ra-salaries/"
              target="_blank"
              >Teaching or research assistant salary schedules</a
            >
          </li>
          <li>
            <a href="https://isc.uw.edu/" target="_blank">Integrated Service Center (ISC)</a>
            <div class="myuw-text-sm text-muted">
              Learn how to
              <a
                href="https://isc.uw.edu/your-time-absence/time-reporting/"
                data-linklabel="ISC Enter Time"
                target="_blank"
                >enter your hours in Workday</a
              >,
              <a
                href="https://isc.uw.edu/your-pay-taxes/paycheck-info/#direct-deposit"
                target="_blank"
                data-linklabel="ISC Set Up direct deposit"
                >set up direct deposit</a
              >, and more.
            </div>
          </li>
        </ul>
      </div>
    </template>
  </uw-card>
</template>

<script>
import { mapState } from 'vuex';
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
  },
  computed: {
    ...mapState({
      employee: (state) => state.user.affiliations.employee,
      faculty: (state) => state.user.affiliations.faculty,
      student: (state) => state.user.affiliations.student,
      studEmployee: (state) => state.user.affiliations.stud_employee,
      instructor: (state) => state.user.affiliations.instructor,
      retire: (state) => state.user.affiliations.retire,
      pastEmployee: (state) => state.user.affiliations.past_employee,
      staticUrl: (state) => state.staticUrl,
    }),
    showCard: function () {
      if (this.isHomePage) {
        return (
          !this.student && !this.instructor && (this.employee || this.retiree || this.pastEmployee)
        );
      }
      return this.studEmployee || this.instructor;
    },
    truncateView: function () {
      return this.retiree || this.pastEmployee;
    },
  },
};
</script>

<style lang="scss" scoped>
// myuw workday button
.myuw-workday {
  background-repeat: no-repeat;
  background-position: 4% 50%;
  background-size: 18px;
  padding-left: 32px;
}
</style>
