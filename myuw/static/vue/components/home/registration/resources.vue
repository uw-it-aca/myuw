<template>
  <div>
    <div v-if="registrationIsOpen" class="my-4 text-center">
      <uw-link-button
        target="_blank"
        title="Register using SLN codes"
        href="https://sdb.admin.uw.edu/students/uwnetid/register.asp"
        class="mb-2"
      >
        Register using SLN codes
      </uw-link-button>
      <div v-if="myplanRegistrationHref" class="d-inline-block">
        <uw-link-button
          target="_blank"
          title="Use MyPlan to Register"
          :href="myplanRegistrationHref"
          class="mb-2"
        >
          Use MyPlan to Register
        </uw-link-button>
      </div>
      <div v-else class="d-inline-block">
        <uw-link-button
          target="_blank"
          title="Use MyPlan to Register"
          :href="`https://myplan.uw.edu/registration/${nextTermYear}${nextTermQuarterCode}`"
          class="mb-2"
        >
          Use MyPlan to Register
        </uw-link-button>
      </div>
      <div v-if="isC2" class="text-center myuw-text-md">
        <a target="_blank" label=""
          href="https://www.degreereg.uw.edu/user-guide">
          How to register for PCE courses
        </a>
      </div>
    </div>
    <div v-else-if="preRegNotices && preRegNotices.length" class="mb-4 text-center">
      <uw-link-button
        target="_blank" label=""
        href="https://sdb.admin.washington.edu/students/uwnetid/op_charges.asp"
        class="mb-2"
      >
        Complete Pre-Registration Requirements
      </uw-link-button>
    </div>
    <div>
      <h4 class="sr-only">Registration resources</h4>
      <ul class="m-0 list-unstyled myuw-text-md">
        <li v-if="!registrationIsOpen">
          <a target="_blank" label=""
            href="https://myplan.uw.edu"
          >
            MyPlan
          </a>
        </li>
        <li v-if="bothell">
          <a target="_blank" label=""
            href="http://www.uwb.edu/registration/time">
            Bothell Time Schedule </a>
        </li>
        <li v-if="seattle">
          <a target="_blank" label=""
            href="http://www.washington.edu/students/timeschd/">
            Seattle Time Schedule
          </a>
        </li>
        <li v-if="tacoma">
          <a target="_blank" label=""
            href="http://www.washington.edu/students/timeschd/T/">
            Tacoma Time Schedule Browse
          </a>
        </li>
        <li v-if="tacoma">
          <a target="_blank" label=""
            href="http://www.tacoma.uw.edu/ts-quicksearch/">
            Tacoma Time Schedule Quick Search
          </a>
        </li>
        <li v-if="isC2">
          <a target="_blank" label=""
            href="https://www.washington.edu/students/timeschd/95index.html">
            PCE Time Schedule
          </a>
        </li>
        <li v-if="isC2 && !registrationIsOpen">
          <a target="_blank" label=""
            href="https://www.degreereg.uw.edu/user-guide">
            How to register for PCE courses
          </a>
        </li>
        <li>
          <a target="_blank" label=""
            :href="degreeAuditHref"> Audit your degree (DARS) </a>
        </li>
        <li>
          <a target="_blank" label=""
            href="https://prereqmap.uw.edu/">Prereq Map</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import LinkButton from '../../_templates/link-button.vue'

export default {
  components: {
    'uw-link-button': LinkButton,
  },
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
      default: () => [],
    },
  },
  computed: {
    ...mapState({
      seattle: (state) => state.user.affiliations.seattle,
      bothell: (state) => state.user.affiliations.bothell,
      tacoma: (state) => state.user.affiliations.tacoma,
      isC2: (state) => state.user.affiliations.grad_c2 || state.user.affiliations.undergrad_c2,
    }),
    currentPlanData() {
      if (this.myPlanData && this.myPlanData.terms) {
        return this.myPlanData.terms.find(
          (term) => term.quarter.toLowerCase() === this.nextTermQuarter.toLowerCase()
        );
      }
      return {};
    },
    myplanRegistrationHref() {
      return this.currentPlanData.registration_href;
    },
    degreeAuditHref() {
      if (this.currentPlanData && this.currentPlanData.degree_audit_href) {
        return this.currentPlanData.degree_audit_href;
      }
      return 'https://myplan.uw.edu/dars';
    },
    nextTermQuarterCode() {
      if (!this.nextTermQuarter || this.nextTermQuarter === 0) {
        return '';
      }
      const q = this.nextTermQuarter.toLowerCase();
      if (q === 'winter') {
        return 1;
      } else if (q === 'spring') {
        return 2;
      } else if (q === 'summer') {
        return 3;
      } else if (q === 'autumn') {
        return 4;
      }

      return '';
    },
  },
};
</script>
