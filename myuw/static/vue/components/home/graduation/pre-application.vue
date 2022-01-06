<template>
  <uw-card
    v-if="showCard"
    v-meta="{term: term}"
    :loaded="isReady">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Graduation Preparation
      </h2>
    </template>
    <template #card-body>
      <p class="myuw-text-md">
        <strong>To graduate, you'll need apply.</strong> Dont worry, it's an easy
        process you complete with your departmental adviser!
      </p>
    </template>
    <template #card-disclosure>
      <b-collapse
        id="collapseGradAppDeadlineAndDetails"
        v-model="isOpen"
      >
        <ul class="list-style myuw-text-md mb-3">
          <li class="mb-1">
            <strong>Deadline:</strong> The third Friday of the quarter
            in which you intend to graduate.
          </li>
          <li class="mb-1">
            <strong>Submit early:</strong> If you apply 2-3 quarters before
            graduation, you get Graduating Senior Priority for registration for 2 quarters.
          </li>
        </ul>

        <p v-if="seattle" class="myuw-text-md">
          <strong>Get all the details:
          <a href="https://www.washington.edu/students/graduation-checklist/">Follow the UW Seattle Graduation checklist</a>.
          </strong> 
        </p>
        <p v-if="tacoma" class="myuw-text-md">
          <strong>Get an
          <a href="https://www.tacoma.uw.edu/registrar/graduation-procedures">
            overview of the UW Tacoma graduation process</a>.
          </strong> 
        </p>
        <p v-if="bothell" class="myuw-text-md">
          <strong>Get all the details on
          <a href="https://www.uwb.edu/registration/graduation">
            UW Bothell’s Graduation, Diplomas, and Commencement page</a>.
          </strong> 
        </p>
        <p v-if="bothell && intlStudent" class="myuw-text-md">
          International students, may find
          <a href="https://www.uwb.edu/cie/alumni">
            additional graduation guidance
          </a> at the Center for International Education.
        </p>
        <p v-if="seattle && intlStudent" class="myuw-text-md">
          International students, review the
          <a href="https://iss.washington.edu/resources/final-checklist/">
            ISS Graduation checklist
          </a> for additional guidance.
        </p>
      </b-collapse>
    </template>
    <template #card-footer>
      <button
        v-b-toggle.collapseGradAppDeadlineAndDetails
        type="button"
        class="btn btn-link btn-sm w-100 p-0 text-dark"
      >
        Deadlines and details
        <font-awesome-icon v-if="!isOpen" :icon="faChevronDown" class="align-middle" />
        <font-awesome-icon v-else :icon="faChevronUp" class="align-middle" />
      </button>
    </template>
  </uw-card>
</template>

<script>
// MUWM-5009 Pre-application
import { faChevronUp, faChevronDown } from '@fortawesome/free-solid-svg-icons';
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
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
      quarter: (state) => state.termData.quarter,
      year: (state) => state.termData.year,
      intlStudent: (state) => state.user.affiliations.intl_stud,
      classLevel: (state) => state.user.affiliations.class_level,
      seattle: (state) => state.user.affiliations.seattle,
      bothell: (state) => state.user.affiliations.bothell,
      tacoma: (state) => state.user.affiliations.tacoma,
    }),
    ...mapState('profile', {
      degreeStatus: (state) => state.value.degree_status,
    }),
    showCard() {
      return (this.isReady && this.degreeStatus.error_code === 404);
    },
    term() {
      return this.year + ',' + this.quarter;
    }
  },
  created() {
    if (this.classLevel === 'SENIOR') this.fetch();
  },
  methods: {
    ...mapActions('profile', ['fetch']),
  },
};
</script>

<style lang="scss" scoped>
</style>
