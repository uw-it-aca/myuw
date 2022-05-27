<template>
  <uw-card
    v-if="showCard"
    :loaded="showContent"
    :errored="showError"
  >
    <template #card-heading>
      <h2 v-if="hasGrantedDegree" class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Congratulations, You've Graduated!
      </h2>
      <h2 v-else class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Graduation Preparation
      </h2>
    </template>
    <template #card-body>
      <div class="row gx-md-4">
        <div v-if="hasActiveApplication" class="col-12 mb-xl-0">
          <p class="myuw-text-md">
            <strong>You're on your way!</strong> We're here to help you get to the finish line!
          </p>          
        </div>
        <div class="col-12 order-xl-2 col-xl-4 mb-xl-0 mb-3">
          <h3 class="h6 text-dark myuw-font-encode-sans myuw-text-md mb-1">
            Graduation Application Status
          </h3>
          <div>
            <ul class="list-unstyled mb-0 myuw-text-md">
              <li v-for="(degree, j) in degrees" :key="j" class="mb-2">
                <span v-if="hasMisconduct(degree)">
                  <p class="myuw-text-md mb-0">
                    Administrative hold – please contact the graduation office at
                    <a href="mailto:ugradoff@uw.edu" class="internal-link">ugradoff@uw.edu</a>.
                  </p>
                  <span class="badge bg-danger-light fw-normal myuw-text-sm text-dark p-2">
                    {{ degree.title }}
                  </span>
                </span>
                <span v-else-if="isIncomplete(degree)">
                  <p class="myuw-text-md mb-0">
                    <em>Application inactive</em> – please contact your departmental advisor
                  </p>
                  <span class="badge bg-light-gray fw-normal myuw-text-sm text-dark p-2">
                    {{ degree.title }}
                  </span>
                </span>
                <span v-else-if="isGranted(degree)">
                  <p class="myuw-text-md mb-0">
                    <em>Degree granted</em> for {{ degreeTerm(degree) }}
                  </p>
                  <span class="badge bg-success-light fw-normal myuw-text-sm text-dark p-2">
                    {{ degree.title }}
                  </span>
                </span>
                <span v-else>
                  <p class="myuw-text-md mb-0">
                    <em>Application active</em> for {{ degreeTerm(degree) }}
                  </p>
                  <span class="badge bg-success-light fw-normal myuw-text-sm text-dark p-2">
                    {{ degree.title }}
                  </span>
                </span>
              </li>
            </ul>
          </div>
        </div>
        <div class="col-12 order-xl-1 col-xl-8">
          <div v-if="hasActiveApplication">
            <h3 class="h6 myuw-font-encode-sans">
              Get an overview
            </h3>
            <ul class="list-style myuw-text-md">
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
                Review the
                <a href="https://www.tacoma.uw.edu/registrar/graduation-procedures">
                UW Tacoma Graduation Checklist</a> for an overview of tasks.
              </li>
            </ul>
          </div>

          <div v-if="hasActiveApplBeforeEarnedTerm">
            <h3 class="h6 myuw-font-encode-sans">
              Ensure that you stay on track
            </h3>
            <ul class="list-style myuw-text-md">
              <li>
                See what courses you have left - run a <a
                href="https://myplan.uw.edu/audit/#/degree">degree audit (DARS)</a>.
              </li>
              <li>
                Plan your remaining quarters in <a href="https://myplan.uw.edu/">MyPlan</a>
                and with your adviser.
              </li>
              <li>
                <a href="https://myplan.uw.edu/audit/#/plan">Audit your plan</a> to confirm
                your plan will lead you to graduation.
              </li>
            </ul>
          </div>

          <div v-if="hasActiveOrGrantedDegreeDuringEarnedTerm">
            <h3 class="h6 myuw-font-encode-sans">
              Run final degree audits
            </h3>
            <ul class="list-style myuw-text-md">
              <li>
                During and after the final quarter ends, use
                <a href="https://myplan.uw.edu/audit/#/degree">degree audit (DARS)</a>
                to make sure that your final quarter course load will satisfy your degree
                requirements and that all your grades are recorded.
              </li>
              <li>
                Contact your advisor if anything appears inaccurate.
              </li>
            </ul>
          </div>

          <div v-if="hasGrantedDegree">
            <h3 class="h6 myuw-font-encode-sans">
              Post-Graduation Success
            </h3>
            <ul class="list-style myuw-text-md">
              <li>
                Get guidance and resources for
                <a href="https://www.washington.edu/graduation/after-graduation/"
                >after graduation</a>.
              </li>
              <li v-if="bothell">
                Find out how to <a 
                href="https://www.uwb.edu/registration/enrollment-verify"
                >provide degree certification</a>
                to other parties.
              </li>
              <li v-if="seattle && tacoma">
                Find out how to <a 
                href="https://registrar.washington.edu/students/enrollment-and-degree-verification/"
                >provide degree certification</a>
                to other parties.
              </li>
            </ul>
          </div>

          <div v-if="hasActiveOrGrantedDegreeDuringAprilMay">
            <h3 class="h6 myuw-font-encode-sans">
              Choose to take part in commencement ceremony
            </h3>
            <ul class="list-unstyled myuw-text-md">
              <li>
                <button
                  v-uw-collapse.commencementCollapse
                  type="button"
                  class="btn btn-link p-0 border-0 align-top notice-link text-start myuw-text-md"
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
            <h3 class="h6 myuw-font-encode-sans">
              Verify that your information and data will not be lost
            </h3>
            <ul class="list-unstyled myuw-text-md">
              <li>
                <button
                  v-uw-collapse.diplomaCollapse
                  type="button"
                  class="btn btn-link p-0 border-0 align-top notice-link text-start myuw-text-md"
                >How to update your diploma name and mailing address</button>
                <uw-collapse id="diplomaCollapse">
                  <div class="p-3 mt-2 bg-light text-dark notice-body">
                    <p>
                      The Office of the University Registrar will send you an email about one
                      month after graduation with the link to a form where you can log in and
                      enter your diploma name and diploma mailing address.
                    </p>
                    <p>
                      If you do not submit the form by the deadline given in the email,
                      the name on your diploma will default to the name on your official
                      student record which may vary from your preferred name.
                    </p>
                    <p>
                      For more information about diplomas, visit the
                      <a href="https://registrar.washington.edu/students/graduation-diplomas/"
                      >Graduations and Diplomas</a> site.
                    </p>
                  </div>
                </uw-collapse>
              </li>
              <li>
                <button
                  v-uw-collapse.saveWorkCollapse
                  type="button"
                  class="btn btn-link p-0 border-0 align-top notice-link text-start myuw-text-md"
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
                  class="btn btn-link p-0 border-0 align-top notice-link text-start myuw-text-md"
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
      </div>
    </template>
    <template #card-disclosure>
      <uw-collapse id="collapseGradSupportAndHelp" v-model="isOpen">
        <h3 class="h6 myuw-font-encode-sans">
            Get Help and Support
        </h3>
        <p class="myuw-text-md mb-1">
          Moving on from the UW can be overwhelming. If you are worried, confused, or
          uncertain about what is next, you are not alone!
        </p>
        <ul class="myuw-text-md">
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
        <h3 class="h6 myuw-font-encode-sans mb-3">
          Related Husky Experience Toolkit Articles
        </h3>
        <div class="myuw-text-md"
            :class="[$mq == 'desktop' ? 'd-flex justify-content-between' : '']"
        >
          <div class="d-flex"
              :class="[$mq == 'desktop' ? 'flex-column pe-4 mb-0' : 'mb-3']">
            <div class="border border-secondary"
            :class="[$mq != 'desktop' ? 'w-50' : '']">
              <a href="https://my.uw.edu/husky_experience_message?article=how-professional-job-different-being-student">
                <img class="img-fluid" src="/static/hx_toolkit_output/images/How_Professional_Job_Different_From_Student_480.jpg" alt="Urban planning student documenting observations in a downtown Seattle park.">
              </a>
            </div>
            <div :class="[$mq != 'desktop' ? 'w-50 ps-3' : 'pt-2']">
              <a href="https://my.uw.edu/husky_experience_message?article=how-professional-job-different-being-student">
                How a Professional Job is Different from Being a Student
              </a> 
              <br>
              <p class="fst-italic">2 min read</p>
            </div>
          </div>
          <div class="d-flex"
              :class="[$mq == 'desktop' ? 'flex-column px-4 mb-0' : 'mb-3']">
            <div class="border border-secondary"
            :class="[$mq != 'desktop' ? 'w-50' : '']">
              <a href="https://my.uw.edu/husky_experience_message?article=preparing-professional-life">
                <img class="img-fluid" src="/static/hx_toolkit_output/images/preparing_for_professional_life_480.jpg" alt="Student and his mentor working together in a UW Health Sciences lab.">
              </a>
            </div>
            <div :class="[$mq != 'desktop' ? 'w-50 ps-3' : 'pt-2']">
              <a href="https://my.uw.edu/husky_experience_message?article=preparing-professional-life">
                Preparing for a Professional Life
              </a>
              <br>
              <p class="fst-italic">2 min read</p>
            </div>
          </div>
          <div class="d-flex"
            :class="[$mq == 'desktop' ? 'flex-column px-4 mb-0' : 'mb-3']"
          >
            <div class="border border-secondary"
            :class="[$mq != 'desktop' ? 'w-50' : '']">
              <a href="https://my.uw.edu/husky_experience_message?article=between-college-and-career">
                <img class="img-fluid" src="/static/hx_toolkit_output/images/Between_College_Career_480.jpg" alt="Person seated on rock ledge above a road that curves away in opposite directions.">
              </a>
            </div>
            <div :class="[$mq != 'desktop' ? 'w-50 ps-3' : 'pt-2']">
              <a href="https://my.uw.edu/husky_experience_message?article=between-college-and-career">
                Between College and Career
              </a>
              <br>
              <p class="fst-italic">2 min read</p>
            </div>
          </div>
        </div>
          
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
    degreeTerm(degree) {
      return this.titleCaseWord(degree.quarter) + ' ' + degree.year;
    }
  }
};
</script>

<style lang="scss" scoped>
.badge {white-space: normal;}
</style>
