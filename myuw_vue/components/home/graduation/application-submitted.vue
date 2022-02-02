<template>
  <uw-card
    v-if="showCard"
    :loaded="showContent"
    :errored="showError"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Graduation Preparation</h2>
    </template>
    <template #card-body>
      <div class="row">
        <div class="col-8">
          <p><strong>You're on your way!</strong> We're here to help you get to the finish line!</p>
          <div v-if="hasActiveApplication">
            <h3 class="h6 text-dark myuw-font-encode-sans">
              Get an overview
            </h3>
            <ul class="list-style">
              <li v-if="seattle">
                Review the
                <a href="https://www.washington.edu/students/graduation-checklist/">
                  UW Graduation checklist
                </a>
                for an overview of tasks.
              </li>
              <li v-if="seattle && intlStudent">
                International students, review the
                <a href="https://iss.washington.edu/resources/final-checklist/">
                  ISS graduation checklist
                </a>
                for additional guidance.
              </li>
              <li v-if="bothell">
                Get all the details on
                <a href="https://www.uwb.edu/registration/graduation">
                UW Bothell’s Graduation, Diplomas, and Commencement page</a>.
              </li>
              <li v-if="bothell && intlStudent">
                International students, may find
                <a href="https://www.uwb.edu/cie/alumni">
                additional graduation guidance
                </a> at the Center for International Education.
              </li>
               <li v-if="tacoma">
                Get an
                <a href="https://www.tacoma.uw.edu/registrar/graduation-procedures">
                overview of the UW Tacoma graduation process</a>.
              </li>
            </ul>
          </div>

          <div v-if="hasActiveApplBeforeEarnedTerm">
            <h3 class="h6 text-dark myuw-font-encode-sans">
              Ensure that you stay on track
            </h3>
            <ul class="list-style">
              <li>
                See what courses you have left - run a <a
                href="https://myplan.uw.edu/audit/#/degree">degree audit (DARS)</a>.
              </li>
              <li>
                Plan your remaining quarters in <a href="https://myplan.uw.edu/">MyPlan</a>.
              </li>
              <li>
                <a href="https://myplan.uw.edu/audit/#/plan">Audit your plan</a> to confirm
                your plan will lead you to graduation.
              </li>
            </ul>
          </div>

          <div v-if="hasActiveOrGrantedDegreeDuringEarnedTerm">
            <h3 class="h6 text-dark myuw-font-encode-sans">
              Run a final audit
            </h3>
            <ul class="list-style">
              <li>
                Make sure all your grades are recorded and that your final quarter course load satisfies your degree requirements using a <a
                href="https://myplan.uw.edu/audit/#/degree">degree audit (DARS)</a>.
              </li>
            </ul>
          </div>

          <div v-if="hasGrantedDegree">
            <h3 class="h6 text-dark myuw-font-encode-sans">
              Post-Graduation Success
            </h3>
            <ul class="list-style">
              <li>
                Get guidance and resources for
                <a href="https://www.washington.edu/graduation/after-graduation/"
                >after graduation</a>.
              </li>
              <li>
                Find out how to <a href="https://registrar.washington.edu/students/enrollment-and-degree-verification/">provide degree certification</a>
                to other parties.
              </li>
            </ul>
          </div>

          <div v-if="hasActiveOrGrantedDegreeDuringAprilMay">
            <h3 class="h6 text-dark myuw-font-encode-sans">
              Choose to take part in commencement ceremony
            </h3>
            <ul class="list-unstyled">
              <li>
                <button
                  v-uw-collapse.commencementCollapse
                  type="button"
                  class="btn btn-link p-0 border-0 align-top notice-link text-start"
                >
                  Decide if you'd like to participate in the UW commencement celebration
                </button>
                <uw-collapse id="commencementCollapse">
                  <div class="p-3 mt-2 bg-light text-dark notice-body">
                    <p v-if="seattle">
                      <a href="https://www.washington.edu/graduation/how-to-participate-2/"
                        >Learn all about commencement</a
                      >, including:
                    </p>
                    <p v-if="bothell">
                      <a href="https://www.uwb.edu/commencement"
                        >Learn all about commencement</a
                      >, including:
                    </p>
                    <p v-if="tacoma">
                      <a href="https://www.tacoma.uw.edu/commencement"
                        >Learn all about commencement</a
                      >, including:
                    </p>
                    <ul class="list-style">
                      <li>Commencement criteria</li>
                      <li>Deadline for registration</li>
                      <li>How to register</li>
                      <li>Ordering cap and gown</li>
                    </ul>
                  </div>
                </uw-collapse>
              </li>
            </ul>
          </div>

          <div v-if="hasActiveOrGrantedDegreeDuringEarnedTerm">
            <h3 class="h6 text-dark myuw-font-encode-sans">
              Verify that your information and data will not be lost
            </h3>
            <ul class="list-unstyled">
              <li>
                <button
                  v-uw-collapse.diplomaCollapse
                  type="button"
                  class="btn btn-link p-0 border-0 align-top notice-link text-start"
                >
                  How to update your diploma name and mailing address
                </button>
                <uw-collapse id="diplomaCollapse">
                  <div class="p-3 mt-2 bg-light text-dark notice-body">
                    <p>
                      The Office of the University Registrar will send you an email about one month after graduation with the link to a 
                      form where you can log in and enter your diploma name and diploma mailing address.
                    </p>
                    <p>
                      If you do not submit the form, the name on your diploma will default to the name on your official student 
                      record which may vary from your preferred name.
                    </p>
                    <p>
                      For more information about diplomas, visit the <a href="https://registrar.washington.edu/students/graduation-diplomas/">Graduations and Diplomas</a> site.
                    </p>
                  </div>
                </uw-collapse>
              </li>
              <li>
                <button
                  v-uw-collapse.saveWorkCollapse
                  type="button"
                  class="btn btn-link p-0 border-0 align-top notice-link text-start"
                >
                  Save your UW work before it is deleted
                </button>
                <uw-collapse id="saveWorkCollapse">
                  <div class="p-3 mt-2 bg-light text-dark notice-body">
                    <p>
                      All UW accounts will be deleted two quarters after graduation.
                      Take steps now to
                      <a href="https://itconnect.uw.edu/students/save-work-before-graduation/"
                      >save all your UW work</a> so that you don't lose it.
                    </p>
                  </div>
                </uw-collapse>
              </li>
              <li>
                <button
                  v-uw-collapse.emailForwardingCollapse
                  type="button"
                  class="btn btn-link p-0 border-0 align-top notice-link text-start"
                >
                  Keep receiving emails sent to your UW address – set up forwarding
                </button>
                <uw-collapse id="emailForwardingCollapse">
                  <div class="p-3 mt-2 bg-light text-dark notice-body">
                    <p>
                      Don't miss critical emails sent to your UW account.
                      <a href="https://uwnetid.washington.edu/manage/?forward"
                      >Set up your email forwarding</a> before you permanently lose access.
                    </p>
                  </div>
                </uw-collapse>
              </li>
            </ul>
          </div>
        </div>
        <div class="col-4">
          <h3 class="h6 text-dark-beige myuw-font-encode-sans">
            Graduation application status
          </h3>
          <div v-if="doubleDegreesInDiffTerms">
            <ul class="list-unstyled mb-0 myuw-text-md">
              <li v-for="(degree, j) in degrees" :key="j" class="mb-1">
                <p v-if="hasMisconduct(degree)" class="myuw-text-md">
                  Administrative hold, please contact the graduation office.
                </p>
                <p v-else-if="isIncomplete(degree)" class="myuw-text-md">
                  Application inactive, please contact your departmental advisor.
                </p>
                <p v-else-if="isGranted(degree)" class="myuw-text-md">
                  Degree granted for {{ degreeTerm(degree) }}
                </p>
                <p v-else class="myuw-text-md">
                  Application active for {{ degreeTerm(degree) }}
                </p>
                <p>
                {{ degree.title }}
                </p>
              </li>
            </ul>
          </div>
          <div v-else-if="doubleDegreeDiffStatus">
            <ul class="list-unstyled mb-0 myuw-text-md">
              <li v-for="(degree, j) in degrees" :key="j" class="mb-1">
                <p v-if="hasMisconduct(degree)" class="myuw-text-md">
                  Administrative hold, please contact the graduation office.
                </p>
                <p v-else-if="isIncomplete(degree)" class="myuw-text-md">
                  Application inactive, please contact your departmental advisor.
                </p>
                <p v-else-if="isGranted(degree)" class="myuw-text-md">
                  Degree granted for {{ degreeTerm(degree) }}
                </p>
                <p v-else>
                  Application active for {{ degreeTerm(degree) }}
                </p>
                <p>
                  {{ degree.title }}
                </p>
              </li>
            </ul>
          </div>
          <div v-else>
            <p v-if="hasMisconduct(degrees[0])" class="myuw-text-md">
              Administrative hold, please contact the graduation office.
            </p>
            <p v-else-if="isIncomplete(degrees[0])" class="myuw-text-md">
              Application inactive, please contact your departmental advisor.
            </p>
            <p v-else-if="isGranted(degrees[0])" class="myuw-text-md">
              Degree granted for {{ degreeTerm(degrees[0]) }}
            </p>
            <p v-else>
              Application active for {{ degreeTerm(degrees[0]) }}
            </p>
            <ul class="list-unstyled mb-0 myuw-text-md">
              <li v-for="(degree, j) in degrees" :key="j" class="mb-1">
                <p>{{ degree.title }}</p>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </template>
    <template #card-disclosure>
      <uw-collapse id="collapseGradSupportAndHelp" v-model="isOpen">
        <h3 class="h6 text-dark-beige myuw-font-encode-sans">
            Get Help and Support
        </h3>
        <p>
          Moving on from the UW can be overwhelming. If you are worried, confused, or
          uncertain about what is next, you are not alone!
        </p>
        <ul>
          <li v-if="seattle">
            <a
              href="http://www.washington.edu/uaa/advising/degree-overview/majors/advising-offices-by-program/"
            >Departmental advisor</a> - graduation and academic support
          </li>
          <li v-if="bothell">
            <a
              href="https://www.uwb.edu/advising"
            >Departmental advisor</a> - graduation and academic support
          </li>
          <li v-if="tacoma">
            <a
              href="https://www.tacoma.uw.edu/gaa"
            >Departmental advisor</a> - graduation and academic support
          </li>
          <li v-if="seattle">
            <a href="https://careers.uw.edu/">Career and Internship Center</a>
            - career consulting
          </li>
          <li v-if="bothell">
            <a href="https://www.uwb.edu/careers">Career and Internship Center</a>
            - career consulting
          </li>
          <li v-if="tacoma">
            <a href="https://www.tacoma.uw.edu/career">Career and Internship Center</a>
            - career consulting
          </li>
          <li v-if="seattle">
            <a href="https://www.washington.edu/financialaid/">Office of Student Financial Aid</a>
            - financial management consulting
          </li>
          <li v-if="bothell">
            <a href="https://www.uwb.edu/financial-aid">Office of Student Financial Aid</a>
            - financial management consulting
          </li>
          <li v-if="tacoma">
            <a href="https://www.tacoma.uw.edu/finaid">Office of Student Financial Aid</a>
            - financial management consulting
          </li>
          <li v-if="seattle">
            <a href="https://www.washington.edu/counseling/">Counseling Center</a>
            - If you are anxious about your future or need someone compassionate to talk to about
            your future or anything else, connect with a counselor.
          </li>
           <li v-if="bothell">
            <a href="https://www.uwb.edu/studentaffairs/counseling">Counseling Center</a>
            - If you are anxious about your future or need someone compassionate to talk to about
            your future or anything else, connect with a counselor.
          </li>
          <li v-if="tacoma">
            <a href="https://www.tacoma.uw.edu/paws">Counseling Center</a>
            - If you are anxious about your future or need someone compassionate to talk to about
            your future or anything else, connect with a counselor.
          </li>
        </ul>
      </uw-collapse>
    </template>
    <template #card-footer>
      <button
        v-uw-collapse.collapseGradSupportAndHelp
        type="button"
        class="btn btn-link btn-sm w-100 p-0 text-dark"
      >
        Learn how to get help and support
        <font-awesome-icon v-if="!isOpen" :icon="faChevronDown" class="align-middle" />
        <font-awesome-icon v-else :icon="faChevronUp" class="align-middle" />
      </button>
    </template>
  </uw-card>
</template>

<script>
// MUWM-5010
import { mapGetters, mapState, mapActions } from 'vuex';
import { faChevronUp, faChevronDown } from '@fortawesome/free-solid-svg-icons';
import Card from '../../_templates/card.vue';
import Collapse from '../../_templates/collapse.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-collapse': Collapse,
  },
  data() {
    return {
      isOpen: false,
      faChevronUp,
      faChevronDown,
    };
  },
  computed: {
    ...mapGetters('profile', {
      isFetching: 'isFetching',
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    ...mapState({
      intlStudent: (state) => state.user.affiliations.intl_stud,
      classLevel: (state) => state.user.affiliations.latest_class_level,
    }),
    ...mapState('profile', {
      degreeStatus: (state) => state.value.degree_status,
      localAddress: (state) => state.value.local_address,
      permanentAddress:  (state) => state.value.permanent_address,
    }),
    graduatingSenior() {
      return (this.classLevel === 'SENIOR');
    },
    showCard() {
      return (this.graduatingSenior &&
        (this.isFetching || this.showContent || this.showError));
    },
    showContent() {
      // having a non-empty degree status
      return (
        this.degreeStatus && this.degreeStatus.degrees &&
        this.degreeStatus.degrees.length > 0);
    },
    showError() {
      // if fetching profile having any error or degree status has a non-404 error
      return (
        this.isErrored ||
        this.degreeStatus && this.degreeStatus.error_code &&
        this.degreeStatus.error_code !== 404);
    },
    degrees() {
      return this.degreeStatus ? this.degreeStatus.degrees : null;
    },
    hasDoubleDegrees() {
      return this.degrees && this.degrees.length > 1
    },
    doubleDegreeDiffStatus() {
      return (
        this.hasDoubleDegrees &&
        (this.hasMisconduct(this.degrees[0]) && !this.hasMisconduct(this.degrees[1]) ||
         this.isIncomplete(this.degrees[0]) && !this.isIncomplete(this.degrees[1]) ||
         this.isActive(this.degrees[0]) && !this.isActive(this.degrees[1]) ||
         this.isGranted(this.degrees[0]) && !this.isGranted(this.degrees[1])));
    },
    doubleDegreesInDiffTerms() {
      return (
        this.hasDoubleDegrees &&
        !(this.degrees[0].quarter == this.degrees[1].quarter &&
          this.degrees[0].year  == this.degrees[1].year));
    },
    mailingAddree() {
      if (!this.degrees) return '';
      return (this.degrees[0].diploma_mail_to_local_address
        ? this.localAddress : this.permanentAddress);
    },
    diplomaName() {
      if (!this.degrees) return '';
      return this.degrees[0].name_on_diploma;
    },
    // The properties below are true as long as one degree status satifies the condition
    hasActiveOrGrantedDegreeDuringAprilMay() {
      let value = (
          this.degrees && this.degrees[0].during_april_may && (
            this.isActive(this.degrees[0]) || this.isGranted(this.degrees[0])));
      if (!value && this.hasDoubleDegrees) {
        value = (this.degrees[1].during_april_may && (
            this.isActive(this.degrees[1]) || this.isGranted(this.degrees[1])));
      }
      return value;
    },
    hasActiveOrGrantedDegreeDuringEarnedTerm() {
      let value = (
        this.degrees && this.degrees[0].is_degree_earned_term && (
            this.isActive(this.degrees[0]) || this.isGranted(this.degrees[0])));
      if (!value && this.hasDoubleDegrees) {
        value = (this.degrees[1].is_degree_earned_term && (
            this.isActive(this.degrees[1]) || this.isGranted(this.degrees[1])));
      }
      return value;
    },
    hasActiveApplBeforeEarnedTerm() {
      let value = (this.degrees &&
        this.isActive(this.degrees[0]) && this.degrees[0].before_degree_earned_term);
      if (!value && this.hasDoubleDegrees) {
        value = this.isActive(this.degrees[1]) && this.degrees[1].before_degree_earned_term;
      }
      return value;
    },
    hasActiveApplication() {
      let value = this.degrees && this.isActive(this.degrees[0]);
      if (!value && this.hasDoubleDegrees) {
        value = this.isActive(this.degrees[1]);
      }
      return value;
    },
    hasGrantedDegree() {
      // data available only within 2 terms after degree granted term
      let value = this.degrees && this.isGranted(this.degrees[0]);
      if (!value && this.hasDoubleDegrees) {
        value = this.isGranted(this.degrees[1]);
      }
      return value;
    },
    seattle() {
      let value = this.degrees && this.degrees[0].campus.toUpperCase() === 'SEATTLE';
      if (!value && this.hasDoubleDegrees) {
        value = this.degrees[1].campus.toUpperCase() === 'SEATTLE';
      }
      return value;
    },
    bothell() {
      let value = this.degrees && this.degrees[0].campus.toUpperCase() === 'BOTHELL';
      if (!value && this.hasDoubleDegrees) {
        value = this.degrees[1].campus.toUpperCase() === 'BOTHELL';
      }
      return value;
    },
    tacoma() {
      let value = this.degrees && this.degrees[0].campus.toUpperCase() === 'TACOMA';
      if (!value && this.hasDoubleDegrees) {
        value = this.degrees[1].campus.toUpperCase() === 'TACOMA';
      }
      return value;
    },
  },
  created() {
    if (this.graduatingSenior) this.fetch();
  },
  methods: {
    ...mapActions('profile', ['fetch']),
    hasMisconduct(degree) {
      return degree.is_admin_hold;
    },
    isIncomplete(degree) {
      return degree.is_incomplete;
    },
    isActive(degree) {
      return degree.has_applied;
    },
    isGranted(degree) {
      return degree.is_granted;
    },
    addressLocationString(address) {
      let location = '';
      if (address.city && address.state) {
        location += address.city + ', ' + address.state;
      }
      if (address.postal_code) {
        location += ' ' + address.postal_code;
      }
      if (address.zip_code) {
        location += ' ' + address.zip_code;
      }
      return location;
    },
    degreeTerm(degree) {
      return this.titleCaseWord(degree.quarter) + ' ' + degree.year;
    }
  }
};
</script>

<style lang="scss" scoped></style>
