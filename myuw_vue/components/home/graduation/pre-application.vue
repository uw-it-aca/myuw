<template>
  <uw-card
    v-if="showCard"
    v-meta="{term: term}"
    :loaded="isReady">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Graduation: Pre Application
      </h2>
    </template>
    <template #card-body>
      <p>
        <strong>To graduate, you'll need apply.</strong> Dont worry, it's an easy
        process you complete with your departmental adviser!
      </p>
    </template>
    <template #card-disclosure>
      <uw-collapse
        id="collapseGradAppDeadlineAndDetails"
        v-model="isOpen"
      >
        <ul class="list-style">
          <li>
            <strong>Deadline:</strong> The third Friday of the quarter
            in which you intend to graduate.
          </li>
          <li>
            <strong>Submit early:</strong> If you apply 2-3 quarters before
            graduation, you get Graduating Senior Priority for registration for 2 quarters.
          </li>
        </ul>
        <p>
          <strong>Get all the details:</strong> Follow the
          <a href="https://www.washington.edu/students/graduation-checklist/">
            UW Graduation checklist
          </a>.
        </p>
        <p v-if="intlStudent">
          International students, review the
          <a href="https://iss.washington.edu/resources/final-checklist/">
            ISS Graduation checklist
          </a> for additional guidance.
        </p>
      </uw-collapse>
    </template>
    <template #card-footer>
      <button
        v-uw-collapse.collapseGradAppDeadlineAndDetails
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
      quarter: (state) => state.termData.quarter,
      year: (state) => state.termData.year,
      intlStudent: (state) => state.user.affiliations.intl_stud,
      classLevel: (state) => state.user.affiliations.class_level,
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
