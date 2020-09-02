<template>
  <uw-card v-if="shouldDisplayAtAll"
           :loaded="allDataLoaded" :errored="anyDataErrored"
  >
    <template #card-heading>
      <h3>
        Registration: {{nextTermQuarter}} {{nextTermYear}}
      </h3>
    </template>
    <template #card-body>
      <!-- TODO: test this component with mock data -->
      <uw-est-reg-date 
        :estRegDateNotices="estRegDateNotices"
        :quarter="nextTermQuarter"
      />
      <uw-holds
        :myplanPeakLoad="myplanPeakLoad"
        :regHoldsNotices="regHoldsNotices"
      />
      <uw-myplan
        v-if="!myplanPeakLoad"
        :nextTermYear="nextTermYear"
        :nextTermQuarter="nextTermQuarter"
      />
    </template>
    <template #card-disclosure>
    </template>
    <template #card-footer>
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../../../containers/card.vue';
import EstRegComponent from './estRegDate.vue';
import HoldsComponent from './holds.vue';
import MyPlanComponent from './myplan.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-est-reg-date': EstRegComponent,
    'uw-holds': HoldsComponent,
    'uw-myplan': MyPlanComponent,
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
      myplanPeakLoad: (state) => state.cardDisplayDates.myplan_peak_load,
    }),
    ...mapState('notices', {
      estRegDateNotices: (state) => state.value.filter(
        (notice) => notice.location_tags.includes('est_reg_date'),
      ),
      preRegNotices: (state) => state.value.filter(
        (notice) => notice.location_tags.includes('reg_card_messages'),
      ),
      regHoldsNotices: (state) => state.value.filter(
        (notice) => notice.location_tags.includes('reg_card_holds'),
      ),
    }),
    ...mapState('oquarter', {
      nextTermYear: (state) => state.value.next_term_data.year,
      nextTermQuarter: (state) => state.value.next_term_data.quarter,
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
    shouldDisplayAtAll: function() {
      return (
        this.student &&
        this.isAfterStartOfRegistrationDisplayPeriod &&
        this.isBeforeEndOfRegistrationDisplayPeriod
      );
    },
    allDataLoaded: function() {
      return (
        this.isNoticesReady &&
        this.isQuarterReady &&
        this.isProfileReady
      );
    },
    anyDataErrored: function() {
      return (
        this.isNoticesErrored ||
        this.isQuarterErrored ||
        this.isProfileErrored
      );
    }
  },
  created() {
    this.fetchNotices();
    this.fetchQuarters();
    this.fetchProfile();
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
  },
}
</script>

<style lang="scss" scoped>

</style>