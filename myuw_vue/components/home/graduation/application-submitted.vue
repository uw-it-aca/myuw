<template>
  <uw-card v-if="showCard" :loaded="isReady">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Graduation Preparation</h2>
    </template>
    <template #card-body>
      <div class="row">
        <div class="col-8">
          <p><strong>You're on your way!</strong> We're here to help you get to the finish line!</p>
          <div v-if="hasApprovedDegree">
            <h3 class="h6 text-dark myuw-font-encode-sans">
              Get an Overview
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
              <li v-if="bothell && intlStudent">
                International students, may find
                <a href="https://www.uwb.edu/cie/alumni">
                additional graduation guidance
                </a> at the Center for International Education.
              </li>
            </ul>
          </div>

          <div v-if="hasApprovedDegreeBeforeEarnedTerm">
            <h3 class="h6 text-dark myuw-font-encode-sans">
              Ensure that you stay on track
            </h3>
            <ul class="list-style">
              <li>
                See what courses you have left - run a <a
                href="https://myplan.uw.edu/audit/#/degree">degree audit (DARS)</a>.
              </li>
              <li>
                Plan remaining quarters in <a href="https://myplan.uw.edu/">MyPlan</a>.
              </li>
              <li>
                <a href="https://myplan.uw.edu/audit/#/plan">Audit your plan</a> to confirm
                your plan will lead you to graduation.
              </li>
            </ul>
          </div>

          <div v-if="hasGraduatedDegree">
            <h3 class="h6 text-dark myuw-font-encode-sans">
              Post-Graduation Success
            </h3>
            <ul class="list-style">
              <li>
                
              </li>
              <li>
                
              </li>
            </ul>
          </div>

          <div v-if="hasANoneErrDegreeDuringAprilMay">
            <h3 class="h6 text-dark myuw-font-encode-sans">
              Take part in Commencement Ceremony
            </h3>
            <ul class="list-unstyled">
              <li>
                <button
                  v-uw-collapse.commencementCollapse
                  type="button"
                  class="btn btn-link p-0 border-0 align-top notice-link text-start"
                >
                  Participate in the UW commencement celebration
                </button>
                <uw-collapse id="commencementCollapse">
                  <div class="p-3 mt-2 bg-light text-dark notice-body">
                    <p>
                      <a href="https://www.washington.edu/graduation/how-to-participate-2/"
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

          <div v-if="hasANoneErrDegreeDuringEarnedTerm">
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
                  Review your diploma name and mailing address
                </button>
                <uw-collapse id="diplomaCollapse">
                  <div class="p-3 mt-2 bg-light text-dark notice-body">
                    <p class="fw-bold">Name on your diploma:</p>
                    <p>{{ nameOnDiploma }}</p>
                    <p>
                      You can change your name using the
                      <a href="https://registrar.washington.edu/students/student-forms/"
                        >Diploma Name Request Form</a>.
                    </p>
                    <p class="fw-bold">Diploma will be mailed to:</p>
                    <div v-if="mailingAddree">
                      <div v-if="mailingAddree.street_line1"
                        v-text="mailingAddree.street_line1">
                      </div>
                      <div v-if="mailingAddree.street_line2"
                        v-text="mailingAddree.street_line2">
                      </div>
                      <span v-text="addressLocationString(mailingAddree)" />
                      <div v-if="mailingAddree.country"
                        v-text="mailingAddree.country">
                      </div>
                    </div>

                    <a href="placeholder">Update your mailing address</a>.
                    <p class="mt-4">
                      <span class="fw-bold fst-italic">Diploma timing -</span> Your
                      diploma will be sent 3 to 4 months after you graduate.
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
                      Take steps now to <a
                      href="https://itconnect.uw.edu/students/save-work-before-graduation/"
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
                <p v-if="isApplicationErr(degree)" class="myuw-text-md">
                  There is an issue with your graduation status. Talk to your departmental advisor.
                </p>
                <p v-else-if="isGraduated(degree)" class="myuw-text-md">
                  Graduated {{ degreeTerm(degree) }}
                </p>
                <p v-else class="myuw-text-md">
                  Application approved for {{ degreeTerm(degree) }}
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
                <p v-if="isApplicationErr(degree)" class="myuw-text-md">
                  There is an issue with your graduation status. Talk to your departmental advisor.
                </p>
                <p v-else-if="isGraduated(degree)" class="myuw-text-md">
                  Graduated {{ degreeTerm(degree) }}
                </p>
                <p v-else>
                  Application approved for {{ degreeTerm(degree) }}
                </p>
                <p>
                  {{ degree.title }}
                </p>
              </li>
            </ul>
          </div>
          <div v-else>
            <p v-if="isApplicationErr(degrees[0])" class="myuw-text-md">
              There is an issue with your graduation status. Talk to your departmental advisor.
            </p>
            <p v-else-if="isGraduated(degrees[0])" class="myuw-text-md">
              Graduated {{ degreeTerm(degrees[0]) }}
            </p>
            <p v-else>
              Application approved for {{ degreeTerm(degrees[0]) }}
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
          Moving on from the UW can be overwhelming. If you are worried, confused, or uncertain
          about what is next, you are not alone!
        </p>
        <ul>
          <li>
            <a
              href="http://www.washington.edu/uaa/advising/degree-overview/majors/advising-offices-by-program/"
            >Departmental advisor</a> - graduation and academic support
          </li>
          <li>
            <a href="https://careers.uw.edu/">Career and Internship Center</a> - career consulting
          </li>
          <li>
            <a href="https://www.washington.edu/financialaid/">Office of Student Financial Aid</a> -
            financial management consulting
          </li>
          <li>
            <a href="https://www.washington.edu/counseling/">Counseling Center</a> - If you are
            anxious about your future or need someone compassionate to talk to about your future or
            anything else, connect with a counselor.
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
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    ...mapState({
      intlStudent: (state) => state.user.affiliations.intl_stud,
      classLevel: (state) => state.user.affiliations.class_level,
    }),
    ...mapState('profile', {
      degreeStatus: (state) => state.value.degree_status,
      localAddress: (state) => state.value.local_address,
      permanentAddress:  (state) => state.value.permanent_address,
    }),
    degrees() {
      return this.degreeStatus.degrees;
    },
    showCard() {
      // having at least one degree
      return (this.isReady && this.degreeStatus &&
        !this.degreeStatus.error_code &&
        this.degrees.length > 0);
    },
    hasDoubleDegrees() {
      return this.degrees.length > 1
    },
    doubleDegreeDiffStatus() {
      return (
        this.hasDoubleDegrees &&
        (this.isApplicationErr(this.degrees[0]) && !this.isApplicationErr(this.degrees[1]) ||
         this.isAppoved(this.degrees[0]) && !this.isAppoved(this.degrees[1]) ||
         this.isGraduated(this.degrees[0]) && !this.isGraduated(this.degrees[1])));
    },
    doubleDegreesInDiffTerms() {
      return (
        this.hasDoubleDegrees &&
        !(this.degrees[0].quarter == this.degrees[1].quarter &&
          this.degrees[0].year  == this.degrees[1].year));
    },
    mailingAddree() {
      return (this.degrees[0].diploma_mail_to_local_address
        ? this.localAddress : this.permanentAddress);
    },
    nameOnDiploma() {
      return this.degrees[0].name_on_diploma;
    },
    // The properties below are true as long as one degree status satifies the condition
    hasANoneErrDegreeDuringAprilMay() {
      // exclude status 1-2
      let value = (
          !this.isApplicationErr(this.degrees[0]) && this.degrees[0].during_april_may);
      if (this.doubleDegreesInDiffTerms) {
        value = (value ||
          !this.isApplicationErr(this.degrees[1]) && this.degrees[1].during_april_may);
      }
      return value;
    },
    hasANoneErrDegreeDuringEarnedTerm() {
      // exclude status 1-2
      let value = (
        !this.isApplicationErr(this.degrees[0]) && this.degrees[0].is_degree_earned_term);
      if (this.doubleDegreesInDiffTerms) {
        value = (value ||
          !this.isApplicationErr(this.degrees[1]) && this.degrees[1].is_degree_earned_term);
      }
      return value;
    },
    hasApprovedDegreeBeforeEarnedTerm() {
      let value = (
        this.isAppoved(this.degrees[0]) && this.degrees[0].before_degree_earned_term);
      if (this.doubleDegreesInDiffTerms) {
        value = (value ||
          this.isAppoved(this.degrees[1]) && this.degrees[1].before_degree_earned_term);
      }
      return value;
    },
    hasApprovedDegree() {
      let value = this.isAppoved(this.degrees[0]);
      if (this.hasDoubleDegrees) {
        value = value || this.isAppoved(this.degrees[1]);
      }
      return value;
    },
    hasGraduatedDegree() {
      // data available only within 2 terms after graduation
      let value = this.isGraduated(this.degrees[0]);
      if (this.hasDoubleDegrees) {
        value = value || this.isGraduated(this.degrees[1]);
      }
      return value;
    },
    seattle() {
      let value = this.degrees[0].campus.toUpperCase() === 'SEATTLE';
      if (this.hasDoubleDegrees) {
        value = value || this.degrees[1].campus.toUpperCase() === 'SEATTLE';
      }
      return value;
    },
    bothell() {
      let value = this.degrees[0].campus.toUpperCase() === 'BOTHELL';
      if (this.hasDoubleDegrees) {
        value = value || this.degrees[1].campus.toUpperCase() === 'BOTHELL';
      }
      return value;
    },
    tacoma() {
      let value = this.degrees[0].campus.toUpperCase() === 'TACOMA';
      if (this.hasDoubleDegrees) {
        value = value || this.degrees[1].campus.toUpperCase() === 'TACOMA';
      }
      return value;
    },
  },
  created() {
    this.fetch();
  },
  methods: {
    ...mapActions('profile', ['fetch']),
    isApplicationErr(degree) {
      return degree.is_admin_hold || degree.is_incomplete;
    },
    isAppoved(degree) {
      return degree.has_applied;
    },
    isGraduated(degree) {
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
