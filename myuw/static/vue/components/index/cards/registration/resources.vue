<template>
  <div>
    <div v-if="registrationIsOpen">
      <a
        target="_blank" title="Register using SLN codes"
        href="https://sdb.admin.uw.edu/students/uwnetid/register.asp"
      >
        Register using SLN codes
      </a>

      <div v-if="myPlanData">
        <a 
          v-if="hasReadyCourses"
          target="_blank" title="Edit plan in MyPlan"
          :href="myplanHref"
        >
          Edit Plan in MyPlan
        </a>
        <a 
          v-else
          target="_blank" title="Register using MyPlan"
          :href="myplanRegistrationHref"
        >
          Register using MyPlan
        </a>
      </div>
      <div v-else>
        <a
          target="_blank" title="Register using MyPlan"
          :href="`https://uwstudent.washington.edu/student/myplan/mplogin/netid?rd=/student/myplan/registration/${nextTermYear}${nextTermQuarterCode}`">
          Use MyPlan to Register
        </a>
      </div>

      <div v-if="isC2">
        <a
          target="_blank"
          href="https://www.degreereg.uw.edu/user-guide"
        >
          How to register for PCE courses
        </a>
      </div>
    </div>
    <div v-else-if="preRegNotices && preRegNotices.length">
      <a
        target="_blank"
        href="https://sdb.admin.washington.edu/students/uwnetid/op_charges.asp"
      >
        Complete Pre-Registration Requirements
      </a>
    </div>
    <div>
      <h4>Registration resources</h4>
      <ul>
        <li v-if="!registrationIsOpen">
          <a
            target="_blank"
            href="https://uwstudent.washington.edu/student/myplan/mplogin/netid?rd=/student/myplan/"
          >
            MyPlan
          </a>
        </li>
        <li v-if="bothell">
          <a
            target="_blank"
            href="http://www.uwb.edu/registration/time"
          >
            Bothell Time Schedule
          </a>
        </li>
        <li v-if="seattle">
          <a
            target="_blank"
            href="http://www.washington.edu/students/timeschd/"
          >
            Seattle Time Schedule
          </a>
        </li>
        <li v-if="tacoma">
          <a
            target="_blank"
            href="http://www.washington.edu/students/timeschd/T/"
          >
            Tacoma Time Schedule Browse
          </a>
        </li>
        <li v-if="tacoma">
          <a
            target="_blank"
            href="http://www.tacoma.uw.edu/ts-quicksearch/"
          >
            Tacoma Time Schedule Quick Search
          </a>
        </li>
        <li v-if="isC2 && registrationIsOpen">
          <a
            target="_blank"
            href="https://www.washington.edu/students/timeschd/95index.html"
          >
            PCE Time Schedule
          </a>
        </li>
        <li v-else-if="isC2 && !registrationIsOpen">
          <a
            target="_blank"
            href="https://www.degreereg.uw.edu/user-guide"
          >
            How to register for PCE courses
          </a>
        </li>
        <li>
          <a target="_blank" :href="degreeAuditHref">
            Audit your degree (DARS)
          </a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';

export default {
  props: {
    myPlanData: {
      type: Object,
      default: null,
    },
    nextTermYear: {
      type: Number,
      required: true,
    },
    nextTermQuarter: {
      type: String,
      required: true,
    },
    registrationIsOpen: {
      type: Boolean,
      default: false,
    },
    preRegNotices: {
      type: Array,
      default: [],
    }
  },
  computed: {
    ...mapState({
      seattle: (state) => state.user.affiliations.seattle,
      bothell: (state) => state.user.affiliations.bothell,
      tacoma: (state) => state.user.affiliations.tacoma,
      isC2: (state) => (
        state.user.affiliations.grad_c2 ||
        state.user.affiliations.undergrad_c2
      ),
    }),
    hasReadyCourses() {
      return this.myPlanData.has_ready_courses;
    },
    myplanHref() {
      return this.myPlanData.myplan_href;
    },
    myplanRegistrationHref() {
      return this.myPlanData.registration_href;
    },
    degreeAuditHref() {
      if (this.myPlanData && this.myPlanData.degree_audit_href) {
        return this.myPlanData.degree_audit_href;
      } else {
        return 'https://uwstudent.washington.edu/student/myplan/mplogin/netid?rd=/student/myplan/audit/degree';
      }
    },
    nextTermQuarterCode() {
      if (!this.nextTermQuarter || this.nextTermQuarter === 0) {
        return "";
      }
      var q = this.nextTermQuarter.toLowerCase();
      if(q === "winter") {
          return 1;
      }
      else if(q === "spring") {
          return 2;
      }
      else if(q === "summer") {
          return 3;
      }
      else if(q === "autumn") {
          return 4;
      }
    },
  },
}
</script>

<style lang="scss" scoped>

</style>