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
      <uw-est-reg-date :estRegData="estRegData"/>
      <uw-holds
        v-if="regHoldsNotices && regHoldsNotices.length"
        :myplanPeakLoad="myplanPeakLoad"
        :regHoldsNotices="regHoldsNotices"
      />

      <!-- TODO: implement pending majors and minors-->

      <uw-in-myplan
        v-if="!myplanPeakLoad"
        :nextTermYear="nextTermYear"
        :nextTermQuarter="nextTermQuarter"
      />

      <span v-if="estRegData.estRegDate && estRegData.isMy1stRegDay">
        Registration opens at 6:00AM
      </span>

      <uw-resources 
        :registrationIsOpen="estRegData.noticeMyRegIsOpen || (
          !estRegData.hasEstRegDataNotice &&
          regPeriod1Started
        )"
      />

      <uw-fin-aid v-if="finAidNotices && finAidNotices.length"/>

      <uw-myplan-courses
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
import moment from 'moment';
import {mapGetters, mapState, mapActions} from 'vuex';

import Card from '../../../../containers/card.vue';
import EstRegComponent from './estRegDate.vue';
import FinAidComponent from './finaid.vue';
import HoldsComponent from './holds.vue';
import InMyPlanComponent from './inMyplan.vue';
import MyplanCoursesComponent from './myplanCourses.vue';
import ResourcesComponent from './resources.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-est-reg-date': EstRegComponent,
    'uw-fin-aid': FinAidComponent,
    'uw-holds': HoldsComponent,
    'uw-in-myplan': InMyPlanComponent,
    'uw-myplan-courses': MyplanCoursesComponent,
    'uw-resources': ResourcesComponent,
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
      regPeriod1Started: (state) => state.cardDisplayDates.reg_period1_started,
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
      finAidNotices: function(state) { 
        return this.nextTermQuarter ? state.value.filter(
          (notice) => notice.location_tags.includes(
            'reg_summeraid_avail_title',
          ),
        ) : [];
      },
    }),
    ...mapState('oquarter', {
      nextTermYear: (state) => state.value.next_term_data.year,
      nextTermQuarter: (state) => state.value.next_term_data.quarter,
    }),
    ...mapState('profile', {
      termMinors: (state) => state.value.term_minors,
      termMajors: (state) => state.value.term_majors,
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
    },
    estRegData: function() {
      const estRegData = {};

      this.estRegDateNotices.forEach((notice) => {
        let registrationDate = null;

        // Set registrationDate date to the first date value found in
        // the notice attributes
        notice.attributes.filter((a) => a.name === 'Date')
          .slice(0, 1).forEach((a) => {registrationDate = moment(a.value)});

        notice.attributes
          .filter(
            (a) => a.name === 'Quarter' &&
            a.value === this.nextTermQuarter
          ).slice(0, 1).forEach((a) => {
            estRegData.hasEstRegDataNotice = true;
            estRegData.noticeMyRegIsOpen = notice.my_reg_has_opened;
            estRegData.isMy1stRegDay = notice.is_my_1st_reg_day;
            estRegData.estRegDate = {
              notice: notice,
              date: registrationDate,
            };
          });
      });

      return estRegData;
    },
    pendingMajors: function() {
      return this.retrieveQuarterDegrees(this.termMajors, "majors");
    },
    pendingMinors: function() {
      return this.retrieveQuarterDegrees(this.termMinors, "minors");
    },
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
    retrieveQuarterDegrees(degrees, degreeType) {
      let filteredDegrees = degrees.filter((degree) => (
        degree.quarter.toUpperCase() === this.nextTermQuarter.toUpperCase() &&
        degree.year === this.nextTermYear &&
        degree.degrees_modified &&
        !degree.has_only_dropped
      ));

      if (filteredDegrees && filteredDegrees.length) {
        return filteredDegrees[0][degreeType];
      } else {
        return [];
      }
    }
  },
}
</script>

<style lang="scss" scoped>

</style>