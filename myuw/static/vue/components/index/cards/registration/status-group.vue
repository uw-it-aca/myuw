<template>
  <div>
    <uw-reg-status />
  </div>
</template>

<script>
import Status from './status.vue';

export default {
  components: {
    'uw-reg-status': Status,
  },
  computed: {
    ...mapState({
      student: (state) => state.user.affiliations.student,
      seattle: (state) => state.user.affiliations.seattle,
      bothell: (state) => state.user.affiliations.bothell,
      tacoma: (state) => state.user.affiliations.tacoma,
      isAfterStartOfRegistrationDisplayPeriod: (state) =>
        state.cardDisplayDates.is_after_start_of_registration_display_period,
      isBeforeEndOfRegistrationDisplayPeriod: (state) =>
        state.cardDisplayDates.is_before_end_of_registration_display_period,
      isAfterStartOfSummerRegDisplayPeriodA: (state) =>
        state.cardDisplayDates.is_after_start_of_summer_reg_display_periodA,
      isAfterStartOfSummerRegDisplayPeriod1: (state) =>
        state.cardDisplayDates.is_after_start_of_summer_reg_display_period1,
      myplanPeakLoad: (state) => state.cardDisplayDates.myplan_peak_load,
      regPeriod1Started: (state) => state.cardDisplayDates.reg_period1_started,
    }),
    ...mapState('notices', {
      notices: (state) => state.value,
    }),
    ...mapState('oquarter', {
      nextTermData: (state) => state.value.next_term_data,
    }),
    ...mapState('profile', {
      profile: (state) => state.value,
    }),
    ...mapState('myplan', {
      myplanData: function(state) {
        return state.value[this.nextTermQuarter];
      },
    }),
    ...mapGetters('notices', {
      isNoticesReady: 'isReady',
      isNoticesErrored: 'isErrored',
    }),
    ...mapGetters('oquarter', {
      isQuarterReady: 'isReady',
      isQuarterErrored: 'isErrored',
    }),
    ...mapGetters('profile', {
      isProfileReady: 'isReady',
      isProfileErrored: 'isErrored',
    }),
    ...mapGetters('myplan', {
      isMyPlanReadyTagged: 'isReadyTagged',
      isMyPlanErroredTagged: 'isErroredTagged',
    }),
    isMyPlanReady() {
      return this.isMyPlanReadyTagged(
        `${this.nextTermData.next_term_year}/${this.nextTermData.next_term_quarter}`
      );
    },
    isMyPlanErrored() {
      return this.isMyPlanErroredTagged(
        `${this.nextTermData.next_term_year}/${this.nextTermData.next_term_quarter}`
      );
    },
  },
  created() {
    this.fetchNotices();
    this.fetchQuarters();
    this.fetchProfile();
  },
  watch: {
    isQuarterReady: function(n, o) {
      if (n) {
        this.fetchMyPlan({
          year: this.nextTermData.next_term_year,
          quarter: this.nextTermData.next_term_quarter,
        });
      }
    }
  },
  methods: {
    ...mapActions('notices', {
      fetchNotices: 'fetch',
    }),
    ...mapActions('oquarter', {
      fetchQuarters: 'fetch',
    }),
    ...mapActions('profile', {
      fetchProfile: 'fetch',
    }),
    ...mapActions('myplan', {
      fetchMyPlan: 'fetch',
    }),
  },
}
</script>

<style lang="scss" scoped>

</style>