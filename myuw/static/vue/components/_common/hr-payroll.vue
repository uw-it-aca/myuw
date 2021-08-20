<template>
  <uw-card v-if="showCard" :loaded="true">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">HR and Payroll</h2>
    </template>
    <template #card-body>
      <div style="position: relative" class="mb-4">
        <h3 class="sr-only">Workday</h3>
        <div class="mb-3">
          <uw-link-button
            id="og_workday"
            v-out="'Workday'"
            class="myuw-workday"
            href="https://wd5.myworkday.com/uw/login.htmld"
            :style="`background-image: url(${staticUrl}images/wday_logo.png);`"
            >Sign in to Workday
          </uw-link-button>
        </div>
        <div class="myuw-text-xs mb-1">
          Workday is the University’s cloud-based HR/payroll operations system.
        </div>
        <div class="myuw-text-xs mb-1">
          *Please note: The Medical Centers continue to use Kronos for time-tracking and payroll.
        </div>
      </div>
      <div v-if="!studEmployee">
        <h3 class="h6 text-dark-beige myuw-font-encode-sans">Get Help</h3>
        <ul class="list-unstyled myuw-text-md mb-1">
          <li class="mb-1">
            <a v-if="faculty" href="https://ap.washington.edu/ahr/">Academic HR</a>
            <a v-else href="https://hr.uw.edu/">UW Human Resources</a>
          </li>
          <li class="mb-1">
            <a href="https://isc.uw.edu/">Integrated Service Center (ISC)</a>
            <div v-if="!truncateView" class="myuw-text-xs">
              Learn how to
              <a v-out="'ISC Time Off'"
                 href="https://isc.uw.edu/your-time-absence/time-off/"
              >look up sick and vacation time</a>,
              <a v-out="'ISC Time Reporting'"
                 href="https://isc.uw.edu/your-time-absence/time-reporting/"
              >report time worked</a>,
              <a v-out="'ISC Edit Personal Address'"
                 href="https://isc.uw.edu/user-guides/edit_personal_information/"
              >update personal information</a>, and more.
            </div>
          </li>
        </ul>
      </div>
      <div v-else>
        <h3 class="h6 text-dark-beige myuw-font-encode-sans">Related</h3>
        <ul class="list-unstyled myuw-text-md mb-1">
          <li class="mb-1"><a href="https://hr.uw.edu/">UW Human Resources</a></li>
          <li class="mb-1">
            <a href="https://hr.uw.edu/benefits/insurance/health/graduate-appointees/"
            >Graduate Appointee Insurance Program (GAIP)</a>
          </li>
          <li class="mb-1">
            <a href="https://grad.uw.edu/graduate-student-funding/funding-information-for-departments/administering-assistantships/ta-ra-salaries/"
            >Teaching or research assistant salary schedules</a>
          </li>
          <li class="mb-1">
            <a href="https://isc.uw.edu/">Integrated Service Center (ISC)</a>
            <div class="myuw-text-xs">
              Learn how to
              <a v-out="'ISC Enter Time'"
                 href="https://isc.uw.edu/your-time-absence/time-reporting/"
              >enter your hours in Workday</a>,
              <a v-out="'ISC Set Up direct deposit'"
                 href="https://isc.uw.edu/your-pay-taxes/paycheck-info/#direct-deposit"
              >set up direct deposit</a>, and more.
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
import LinkButton from '../_templates/link-button.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-link-button': LinkButton,
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
      retiree: (state) => state.user.affiliations.retiree,
      pastEmployee: (state) => state.user.affiliations.past_employee,
      staticUrl: (state) => state.staticUrl,
    }),
    showCard () {
      if (this.isHomePage) {
        return this.retiree || this.pastEmployee ||
          this.employee && !this.student && !this.instructor;
      }
      return this.studEmployee || this.instructor;
    },
    truncateView () {
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
