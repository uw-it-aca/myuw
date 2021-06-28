<template>
  <div v-if="applicant && !isErrored">
    <uw-seattle :applicant-data="seattleApplicant" :is-ready="isReady" />
    <!-- <uw-bothell :applicant-data="bothellApplicant" :is-ready="isReady" /> -->
    <uw-tacoma :applicant-data="tacomaApplicant" :is-ready="isReady" />
  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Seattle from './seattle.vue';
// import Bothell from './bothell.vue';
import Tacoma from './tacoma.vue';

export default {
  components: {
    'uw-seattle': Seattle,
    // 'uw-bothell': Bothell,
    'uw-tacoma': Tacoma,
  },
  computed: {
    ...mapState({
      applicant: (state) => state.user.affiliations.applicant,
      seattleApplicant: (state) =>
        state.applicant.value.filter((applicant) => applicant.is_seattle)[0],
      bothellApplicant: (state) =>
        state.applicant.value.filter((applicant) => applicant.is_bothell)[0],
      tacomaApplicant: (state) =>
        state.applicant.value.filter((applicant) => applicant.is_tacoma)[0],
    }),
    ...mapGetters('applicant', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
  },
  mounted() {
    if (this.applicant) this.fetch();
  },
  methods: {
    ...mapActions('applicant', ['fetch']),
  },
};
</script>

