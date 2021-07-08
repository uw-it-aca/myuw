<template>
  <span v-if="showCard">
    <div class="d-flex d-sm-inline-flex notice-container">
      <div class="flex-grow-1 pr-1">
        <span class="notice-title">
          <button
            v-b-toggle.covid_notice
            v-no-track-collapse
            class="btn btn-link p-0 border-0 align-top notice-link text-left myuw-text-md"
          >
            <span class="d-inline-block font-weight-bold text-danger mr-1 notice-critical"
              >Critical:</span
            ><span>Complete the UW Student COVID-19 Vaccine Attestation Form</span>
          </button>
        </span>
      </div>
      <div>
        <b-badge
          variant="warning"
          class="font-weight-normal notice-status"
        >
          New
        </b-badge>
      </div>
    </div>
    <b-collapse id="covid_notice" tabindex="0">
      <div class="p-3 mt-2 mb-2 bg-light text-dark notice-body">
      The University of Washington is requiring all students to be vaccinated
      against COVID-19, with certain exemptions allowed. Please
      <a href="https://uw.edu/studentcovidform">complete the UW Student COVID-19 Vaccine Attestation Form</a> as soon as possible.
      </div>
    </b-collapse>
  </span>
</template>

<script>
import {
  faSyringe,
} from '@fortawesome/free-solid-svg-icons';
import {mapGetters, mapState, mapActions} from 'vuex';

export default {
  data: function() {
    return {
      faSyringe,
    };
  },
  computed: {
    ...mapState({
      student: (state) => state.user.affiliations.student,
    }),
    ...mapState('covid19', {
      covid19: (state) => state.value,
    }),
    ...mapGetters('covid19', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    showCard() {
      return this.student && this.statusCode === 404;
    }
  },
  mounted() {
    this.fetch();
  },
  methods: {
    ...mapActions('covid19', ['fetch']),
  },
};
</script>
