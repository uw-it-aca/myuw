<template>
  <div>
    <div v-if="registrationIsOpen">
      <a
        target="_blank" title="Register using SLN codes"
        href="https://sdb.admin.uw.edu/students/uwnetid/register.asp"
      >
        Register using SLN codes
      </a>

      <div v-if="myplanShouldDisplay && isReady">
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
      <div v-else-if="isReady">
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
    myplanShouldDisplay: {
      type: Boolean,
      default: true,
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
    ...mapState('myplan', {
      hasReadyCourses: function(state) {
        return state.value[this.nextTermQuarter].has_ready_courses;
      },
      myplanHref: function(state) {
        return state.value[this.nextTermQuarter].myplan_href;
      },
      myplanRegistrationHref: function(state) {
        return state.value[this.nextTermQuarter].registration_href;
      },
      degreeAuditHref: function(state) {
        if (this.myplanShouldDisplay && this.isReady) {
          return state.value[this.nextTermQuarter].degree_audit_href;
        } else {
          return 'https://uwstudent.washington.edu/student/myplan/mplogin/netid?rd=/student/myplan/audit/degree';
        }
      },
    }),
    ...mapState({
      seattle: (state) => state.user.affiliations.seattle,
      bothell: (state) => state.user.affiliations.bothell,
      tacoma: (state) => state.user.affiliations.tacoma,
      isC2: (state) => (
        state.user.affiliations.grad_c2 ||
        state.user.affiliations.undergrad_c2
      ),
    }),
    ...mapGetters('myplan', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
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
  created() {
    if (this.myplanShouldDisplay) {
      this.fetchMyPlan({
        year: this.nextTermYear,
        quarter: this.nextTermQuarter
      });
    }
  },
  methods: {
    ...mapActions('myplan', {
      fetchMyPlan: 'fetch',
    }),
  },
}
</script>

<style lang="scss" scoped>

</style>