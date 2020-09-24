<template>
  <div>
    <uw-reg-status
      v-for="quarter in quarters"
      :key="quarter" :quarter="quarter" :year="nextTermData.year"
      :myPlanData="myplanData[`${nextTermData.year}/${quarter}`]"
      :loaded="loaded(quarter)" :errored="errored(quarter)"
      :notices="notices" :profile="profile" :oquarterData="oquarterData"
    />
  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
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
      myPlanPeakLoad: (state) => state.cardDisplayDates.myplan_peak_load,
    }),
    ...mapState('notices', {
      notices: (state) => state.value,
    }),
    ...mapState('oquarter', {
      nextTermData: (state) => state.value.next_term_data || {},
      oquarterData: (state) => Array.isArray(state.value) ? null : state.value,
    }),
    ...mapState('profile', {
      profile: function(state) {
        return this.isProfileReady ? state.value : null;
      },
    }),
    ...mapState('myplan', {
      myplanData: function(state) {
        return state.value || {};
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
    needsSummerCard() {
      return this.isAfterStartOfSummerRegDisplayPeriodA ||
        this.isAfterStartOfSummerRegDisplayPeriod1;
    },
  },
  created() {
    if (this.student) {
      if (this.needsSummerCard) {
        this.quarters.push('Summer');
      }

      if (
        this.isAfterStartOfRegistrationDisplayPeriod &&
        this.isBeforeEndOfRegistrationDisplayPeriod
      ) {
        this.quarters.push(this.nextQuarterStub);
      }

      this.fetchNotices();
      this.fetchQuarters();
      this.fetchProfile();
    }
  },
  data() {
    return {
      quarters: [],
      nextQuarterStub: 'Next',
    };
  },
  watch: {
    isQuarterReady: function(n, o) {
      if (!o && n && !this.myPlanPeakLoad) {
        if (this.needsSummerCard) {
          this.fetchMyPlan({
            year: this.nextTermData.year,
            quarter: 'Summer',
          });
        }

        if (this.quarters.indexOf(this.nextQuarterStub) !== -1) {
          // Replace the stub with the real quarter
          this.quarters.splice(
            this.quarters.indexOf(this.nextQuarterStub),
            1,
            this.nextTermData.quarter,
          )
          this.fetchMyPlan({
            year: this.nextTermData.year,
            quarter: this.nextTermData.quarter,
          });
        }
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
    loaded(quarter) {
      return (
        this.isNoticesReady &&
        this.isQuarterReady &&
        this.isProfileReady &&
        (
          this.myplanPeakLoad ||
          (!this.myplanPeakLoad && this.isMyPlanReadyTagged(
            `${this.nextTermData.year}/${quarter}`
          ))
        )
      );
    },
    errored(quarter) {
      return (
        this.isNoticesErrored ||
        this.isQuarterErrored ||
        this.isProfileErrored ||
        (!this.myplanPeakLoad && this.isMyPlanErroredTagged(
          `${this.nextTermData.year}/${quarter}`
        ))
      );
    },
  },
}
</script>

<style lang="scss" scoped>

</style>