<template>
  <div>
    <div v-if="showComPreReg" class="mb-4 text-center">
      <uw-link-button
        :href="registrationHref"
        class="mb-2"
      >
        Complete Pre-Registration Requirements
      </uw-link-button>
      <div class="text-center myuw-text-sm pb-3 fst-italic">
        You will not be able to register until you complete Pre-Registration
      </div>
    </div>
    <div v-if="registrationIsOpen" class="my-4 text-center">
      <uw-link-button
        :href="registrationHref"
        class="mb-2"
      >
        Go to Register.UW
      </uw-link-button>
      <div class="text-center myuw-text-sm pb-3 fst-italic">
        You will be able to import your ready planned items from MyPlan
      </div>
      <div v-if="isC2" class="text-center myuw-text-md">
        <a
          href="https://www.degreereg.uw.edu/how-to-register">
          How to register for PCE courses
        </a>
      </div>
    </div>
    <div v-else-if="preRegCompleted" class="mb-4 text-center myuw-text-md">
      You have completed all pre-registration requirements for
      {{ nextTermQuarter }} {{ nextTermYear }}. <br />
      <a href="https://uwconnect.uw.edu/it?id=kb_article_view&sysparm_article=KB0035391"
      >Learn about registration</a>
      or <a title="build schedule in MyPlan"
      href="https://myplan.uw.edu/plan/">build your schedule in MyPlan</a>
    </div>

    <div>
      <h3 class="visually-hidden">Registration resources</h3>
      <ul class="m-0 list-unstyled myuw-text-md">
        <li v-if="!registrationIsOpen" class="mb-1">
          <a href="https://myplan.uw.edu"> MyPlan </a>
        </li>
        <li v-if="bothell" class="mb-1">
          <a href="https://www.uwb.edu/registrar/time">
            Bothell Time Schedule
          </a>
        </li>
        <li v-if="seattle" class="mb-1">
          <a href="https://www.washington.edu/students/timeschd/">
            Seattle Time Schedule
          </a>
        </li>
        <li v-if="tacoma" class="mb-1">
          <a href="https://www.washington.edu/students/timeschd/T/">
            Tacoma Time Schedule Browse
          </a>
        </li>
        <li v-if="tacoma" class="mb-1">
          <a href="https://www.tacoma.uw.edu/ts-quicksearch/">
            Tacoma Time Schedule Quick Search
          </a>
        </li>
        <li v-if="isC2" class="mb-1">
          <a
            href="https://www.washington.edu/students/timeschd/95index.html"
          >
            PCE Time Schedule
          </a>
        </li>
        <li v-if="isC2 && !registrationIsOpen" class="mb-1">
          <a href="https://www.degreereg.uw.edu/how-to-register">
            How to register for PCE courses
          </a>
        </li>
        <li class="mb-1">
          <a :href="degreeAuditHref"> Audit your degree (DARS) </a>
        </li>
        <li class="mb-1">
          <a href="https://dawgpath.uw.edu">DawgPath</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import LinkButton from '../../_templates/link-button.vue';

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
    registrationHref() {
      // MyPlan returns quarter specific registration href
      return this.currentPlanData.registration_href;
    },
    degreeAuditHref() {
      if (this.currentPlanData && this.currentPlanData.degree_audit_href) {
        return this.currentPlanData.degree_audit_href;
      }
      return 'https://myplan.uw.edu/audit/#/degree';
    },
    preRegCompleted() {
      // MUWM-5401
      return (this.preRegNotices && this.preRegNotices.length > 0 &&
        this.currentPlanData && this.currentPlanData.complete_pre_reg);
    },
    showComPreReg() {
      // MUWM-5395
      // The display window is determined by the preRegNotices
      // and show/no-show by complete_pre_reg
      return (this.preRegNotices && this.preRegNotices.length > 0 &&
        this.currentPlanData && !this.currentPlanData.complete_pre_reg);
    },
  },
};
</script>
