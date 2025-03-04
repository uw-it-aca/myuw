<template>
  <div v-if="applicant">
    <div v-if="!isErrored">
      <uw-seattle :applicant-data="seaApplication" :is-ready="isReady" />
      <uw-bothell v-if="isBotReturning" :applicant-data="botApplication" :is-ready="isReady" />
      <uw-tacoma :applicant-data="tacApplication" :is-ready="isReady" />
    </div>
    <uw-card v-else :loaded="showError" :errored="showError" :errored-show="showError">
      <template #card-heading>
        <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Application Information</h2>
      </template>
      <template #card-error>
        An error occurred and MyUW cannot load your status right now. In the meantime,
        you may find what you need on the
        <a href="https://sdb.admin.uw.edu/admissions/uwnetid/appstatus.asp">
          Application Status
        </a> page.
      </template>
    </uw-card>
  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Seattle from './seattle.vue';
import Bothell from './bothell.vue';
import Tacoma from './tacoma.vue';

export default {
  components: {
    'uw-seattle': Seattle,
    'uw-bothell': Bothell,
    'uw-tacoma': Tacoma,
  },
  data() {
    return {
      duringAdmissionDecissionRelease: true,
      // make this configureble in the future
    };
  },
  computed: {
    ...mapState({
      applicant: (state) => state.user.affiliations.applicant,
    }),
    ...mapState('applicant', {
      application: (state) => state.value,
    }),
    ...mapGetters('applicant', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    botApplication() {
      return this.application.filter((item) => item.is_bothell)[0];
    },
    seaApplication() {
      return this.application.filter((item) => item.is_seattle)[0];
    },
    tacApplication() {
      return this.application.filter((item) => item.is_tacoma)[0];
    },
    isBotReturning() {
      return this.botApplication && this.botApplication.is_returning;
    },
    showError() {
      // MUWM-5391
      return this.duringAdmissionDecissionRelease && this.statusCode !== 404;
    },
  },
  created() {
    if (this.applicant) this.fetch();
  },
  methods: {
    ...mapActions('applicant', ['fetch']),
  },
};
</script>
