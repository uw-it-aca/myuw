<template>
  <uw-card v-if="showCard" :loaded="isReady">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Graduation Preparation</h2>
    </template>
    <template #card-body>
      <div class="row">
        <div class="col-8">
          <p><strong>You're on your way!</strong> We're here to help you get to the finish line!</p>
          <p class="myuw-text-lg mb-0">Get an overview</p>
          <ul class="list-style">
            <li>
              Review the
              <a href="https://www.washington.edu/students/graduation-checklist/">
                UW Graduation checklist
              </a>
              for an overview of tasks.
            </li>
            <li>
              International students, review the
              <a href="https://iss.washington.edu/resources/final-checklist/">
                ISS graduation checklist
              </a>
              for additional guidance.
            </li>
          </ul>
          <p class="myuw-text-lg mb-0">Take part in the commencement ceremony</p>
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
                    <a href="https://www.washington.edu/graduation/how-to-participate-2/">Learn all about commencement</a>, including:
                  </p>
                  <ul class="list-style">
                    <li>
                      Commencement criteria
                    </li>
                    <li>
                      Deadline for registration
                    </li>
                    <li>
                      How to register
                    </li>
                    <li>
                      Ordering cap and gown
                    </li>
                  </ul>
                </div>
              </uw-collapse>
            </li>
          </ul>
          <p class="myuw-text-lg mb-0">Verify that your information and data will not be lost</p>
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
                <div class="p-3 mt-2 bg-light text-dark notice-body"><h3>hello!</h3></div>
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
                <div class="p-3 mt-2 bg-light text-dark notice-body"><h3>hello!</h3></div>
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
                <div class="p-3 mt-2 bg-light text-dark notice-body"><h3>hello!</h3></div>
              </uw-collapse>
            </li>
          </ul>
        </div>
        <div class="col-4">
          <h3 class="h6 text-dark-beige myuw-font-encode-sans">Graduation application status</h3>
          <p v-if="isApproved(degrees[0].status)" class="myuw-text-md">
            Approved for {{ titleCaseWord(degrees[0].quarter) }} {{ degrees[0].year }} graduation
          </p>
          <p v-else class="myuw-text-md">
            There is an issue with your graduation status. Talk to your departmental advisor.
          </p>
          <h3 class="h6 text-dark-beige myuw-font-encode-sans">
            Intended degree<span v-if="degrees.length > 1">s</span>
          </h3>
          <ul class="list-unstyled mb-0 myuw-text-md">
            <li v-for="(degree, j) in degrees" :key="j" class="mb-1">
              {{ degree.title }}
            </li>
          </ul>
        </div>
      </div>
    </template>
    <template #card-disclosure>
      <uw-collapse id="collapseGradSupportAndHelp" v-model="isOpen">
        <p class="myuw-text-lg text-dark-beige mb-0">Get Help and Support</p>
        <p>
          Moving on from the UW can be overwhelming. If you are worried, confused, or uncertain
          about what is next, you are not alone!
        </p>
        <ul>
          <li>
            <a
              href="http://www.washington.edu/uaa/advising/degree-overview/majors/advising-offices-by-program/"
              >Departmental advisor</a
            >
            - graduation and academic support
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
// MUWM-5009
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
    }),
    showCard() {
      return this.isReady && !this.degreeStatus.error_code;
    },
    degrees() {
      return this.degreeStatus.degrees;
    },
  },
  created() {
    if (this.classLevel === 'SENIOR') this.fetch();
  },
  methods: {
    ...mapActions('profile', ['fetch']),
    isApproved(status) {
      return status >= 3 && status <= 5;
    },
  },
};
</script>

<style lang="scss" scoped></style>
