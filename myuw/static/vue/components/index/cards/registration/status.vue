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
        :myplanPeakLoad="myplanShouldDisplay"
        :regHoldsNotices="regHoldsNotices"
      />

      <div>
        <h4 v-if="pendingMajors.length">
          {{pendingMajors.length > 1 ? "Majors" : "Major"}}
          Beginning <br>
          {{nextTermQuarter}}
        </h4>
        <span v-for="(major, i) in pendingMajors" :key="i">
          {{major.degree_abbr}}
        </span>
      </div>

      <div>
        <h4 v-if="pendingMinors.length">
          {{pendingMinors.length > 1 ? "Minors" : "Minor"}}
          Beginning <br>
          {{nextTermQuarter}}
        </h4>
        <span v-for="(minor, i) in pendingMinors" :key="i">
          {{minor.abbr}}
        </span>
      </div>

      <uw-in-myplan
        v-if="myplanShouldDisplay"
        :nextTermYear="nextTermYear"
        :nextTermQuarter="nextTermQuarter"
      />

      <span v-if="estRegData.estRegDate && estRegData.isMy1stRegDay">
        Registration opens at 6:00AM
      </span>

      <uw-resources
        :myplanShouldDisplay="myplanShouldDisplay"
        :registrationIsOpen="estRegData.noticeMyRegIsOpen || (
          !estRegData.hasEstRegDataNotice &&
          regPeriod1Started
        )"
        :nextTermYear="nextTermYear"
        :nextTermQuarter="nextTermQuarter"
        :preRegNotices="preRegNotices"
      />

      <uw-fin-aid 
        v-if="finAidNotices && finAidNotices.length && isSummerReg"
        :finAidNotices="finAidNotices"
      />
    </template>
    <template v-if="myplanShouldDisplay" #card-disclosure>
      <b-collapse id="myplan-courses-collapse" v-model="isOpen">
        <uw-myplan-courses
          :nextTermYear="nextTermYear"
          :nextTermQuarter="nextTermQuarter"
        />
      </b-collapse>
    </template>
    <template v-if="myplanShouldDisplay" #card-footer>
      <b-button
        v-if="!isOpen"
        v-b-toggle.myplan-courses-collapse
        :aria-label="
          `Expand to show your ${nextTermQuarter} ${nextTermYear} plan`
        "
        variant="link"
        size="sm"
        class="w-100 p-0 text-dark"
      >
        <!-- TODO: @charlon add a css capital class for this button -->
        SHOW {{nextTermQuarter}} {{nextTermYear}} PLAN
      </b-button>
      <b-button
        v-else
        v-b-toggle.myplan-courses-collapse
        :aria-label="
          `Collapse to hide your ${nextTermQuarter} ${nextTermYear} plan`
        "
        variant="link"
        size="sm"
        class="w-100 p-0 text-dark"
      >
        <!-- TODO: @charlon add a css capital class for this button -->
        HIDE {{nextTermQuarter}} {{nextTermYear}} PLAN
      </b-button>
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
      hasRegistration: (state) => state.value.next_term_data.has_registration,
    }),
    ...mapState('profile', {
      termMinors: (state) => state.value.term_minors,
      termMajors: (state) => state.value.term_majors,
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
      isMyPlanReady: 'isReady',
      isMyPlanErrored: 'isErrored',
    }),
    shouldDisplayAtAll: function() {
      return (
        this.student &&
        this.isAfterStartOfRegistrationDisplayPeriod &&
        this.isBeforeEndOfRegistrationDisplayPeriod &&
        (
          (
            this.allDataLoaded && 
            !(this.isSummerReg && this.hasRegistration) && (
              // Can do any one of these
              (this.finAidNotices && this.finAidNotices.length) ||
              this.estRegData.estRegDate ||
              (this.regHoldsNotices && this.regHoldsNotices.length) ||
              this.myplanShouldDisplay
            )
          ) || !this.allDataLoaded
        )
      );
    },
    allDataLoaded: function() {
      return (
        this.isNoticesReady &&
        this.isQuarterReady &&
        this.isProfileReady &&
        (
          this.myplanPeakLoad ||
          (!this.myplanPeakLoad && this.isMyPlanReady)
        )
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
    isSummerReg: function() {
      return this.nextTermQuarter === "Summer";
    },
    myplanShouldDisplay: function() {
      return (
        !this.myplanPeakLoad &&
        this.isMyPlanReady &&
        this.myplanData !== undefined
      );
    }
  },
  created() {
    this.fetchNotices();
    this.fetchQuarters();
    this.fetchProfile();
  },
  data() {
    return {
      isOpen: false,
    }
  },
  watch: {
    isQuarterReady: function(n, o) {
      if (n) {
        this.fetchMyPlan({
          year: this.nextTermYear,
          quarter: this.nextTermQuarter
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