<template>
  <uw-card v-if="showCard" :loaded="isReady">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Graduation Preparation</h2>
    </template>
    <template #card-body>
      <div class="row">
        <div class="col-8">
          <p>
            <strong>You're on your way!</strong> We're here to help you get to the finish line!
          </p>
          <p class = myuw-text-lg>
            Get an overview
          </p>
          <ul class="list-style">
            <li>Review the
              <a href="https://www.washington.edu/students/graduation-checklist/">
              UW Graduation checklist
              </a> for an overview of tasks.
            </li>
            <li>International students, review the
              <a href="https://iss.washington.edu/resources/final-checklist/">
              ISS graduation checklist
              </a> for additional guidance.
            </li>
          </ul>
          <p class = myuw-text-lg>
            Take part in the commencement ceremony
          </p>
          <p class = myuw-text-lg>
            Verify that your information and data will not be lost
          </p>
          <ul>
            <li>
              <button v-uw-collapse.myCollapseId type="button" class="btn btn-link p-0 border-0 align-top notice-link text-start myuw-text-md">Review your diploma name and mailing address</button>
              <uw-collapse id="myCollapseId">
                <div class="p-3 mt-2 bg-light text-dark notice-body"> <h3>hello!</h3> </div>
              </uw-collapse>
            </li>
            <li>Save your UW work before it is deleted</li>
            <li>Keep receiving emails sent to your UW address – set up forwarding</li>
          </ul>
        </div>
        <div class="col-4">
          <h3 class="h6 text-dark-beige myuw-font-encode-sans">
            Graduation application status
          </h3>
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
      <uw-collapse
        id="collapseGradSupportAndHelp"
        v-model="isOpen"
      >
        <p>this is the disclosure content</p>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Debitis dolorem labore a sit
          placeat nisi iusto ullam, ipsam vitae numquam ad, magni at ex quas ut magnam dignissimos
          incidunt nostrum.
        </p>
      </uw-collapse>
    </template>
    <template #card-footer>
      <button
        v-uw-collapse.collapseGradSupportAndHelp
        type="button"
        class="btn btn-link btn-sm w-100 p-0 text-dark"
      >
        Learn how to get support and help
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
      return (this.isReady && !this.degreeStatus.error_code);
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
      return (status >= 3 && status <= 5);
    },
  }
};
</script>

<style lang="scss" scoped>
</style>
