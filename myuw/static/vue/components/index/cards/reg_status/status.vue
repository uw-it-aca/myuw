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

export default {
  components: {
    'uw-card': Card,
  },
  computed: {
    ...mapState({
      student: (state) => state.user.affiliations.student,
      isAfterStartOfRegistrationDisplayPeriod: (state) =>
        state.cardDisplayDates.is_after_start_of_registration_display_period,
      isBeforeEndOfRegistrationDisplayPeriod: (state) =>
        state.cardDisplayDates.is_before_end_of_registration_display_period,
    }),
    ...mapState('notices', {
      estRegDateNotices: (state) => state.value.filter(
        (notice) => notice.location_tags.includes('est_reg_date'),
      ),
      preRegNotices: 
    }),
    ...mapState('oquarter', {
      nextTermYear: (state) => state.value.next_term_data.year,
      nextTermQuarter: (state) => state.value.next_term_data.quarter,
    }),
    ...mapState('profile', {
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
      return this.isNoticesReady && this.isQuarterReady && this.isProfileReady;
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