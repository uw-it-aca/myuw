<template>
  <span v-if="showCard">
    <div class="d-flex d-sm-inline-flex notice-container">
      <div class="flex-grow-1 pe-1">
        <span class="notice-title">
          <button
            v-uw-collapse.covid_notice
            v-no-track-collapse
            class="btn btn-link p-0 border-0 align-top notice-link text-start myuw-text-md"
          >
            <span class="d-inline-block fw-bold text-danger me-1 notice-critical"
              >Critical:</span
            ><span>Complete the UW Student COVID-19 Vaccine Attestation Form</span>
          </button>
        </span>
      </div>
      <div>
        <span class="badge bg-warning fw-normal notice-status text-dark p-1">
          New
        </span>
      </div>
    </div>
    <uw-collapse id="covid_notice" tabindex="0">
      <div class="p-3 mt-2 mb-2 bg-light text-dark notice-body">
      The University of Washington is requiring all students to be vaccinated
      against COVID-19, with certain exemptions allowed. Please
      <a href="https://uw.edu/studentcovidform">complete the UW Student COVID-19 Vaccine Attestation Form</a> as soon as possible.
      </div>
    </uw-collapse>
  </span>
</template>

<script>
import {
  faSyringe,
} from '@fortawesome/free-solid-svg-icons';
import {mapGetters, mapState, mapActions} from 'vuex';
import Collapse from '../../_templates/collapse.vue';

export default {
  components: {
    'uw-collapse': Collapse,
  },
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
  created() {
    if (this.student) this.fetch();
  },
  methods: {
    ...mapActions('covid19', ['fetch']),
  },
};
</script>
