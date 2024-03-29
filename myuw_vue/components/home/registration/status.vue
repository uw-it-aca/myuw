<template>
  <uw-card
    v-if="shouldDisplayAtAll && (!loaded || hasDataToDisplay)"
    v-meta="{term: loaded ? `${year},${quarter}` : null}"
    :loaded="loaded"
    :errored="errored"
    :errored-show="!isSummerReg || (isSummerReg && period === 'A')"
  >
    <template #card-heading>
      <h2 v-if="!errored" class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Registration: {{ quarter }} {{ year }}
      </h2>
      <h2 v-else class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        {{ forQuarter }} Registration
      </h2>
    </template>
    <template #card-body>

      <uw-est-reg-date :est-reg-data="estRegData" />
      <uw-holds
        v-if="regHoldsNotices && regHoldsNotices.length"
        :reg-holds-notices="regHoldsNotices"
      />

      <div v-if="pendingMajors.length" class="mb-4">
        <uw-card-status>
          <template #status-label>
            {{ pendingMajors.length > 1 ? 'Majors' : 'Major' }}
            Beginning <br>
            {{ quarter }}
          </template>
          <template #status-value>
            <span
              v-for="(major, i) in pendingMajors"
              :key="i"
              class="fw-bold"
            >
              {{ major.degree_abbr }}
            </span>
          </template>
        </uw-card-status>
      </div>

      <div v-if="pendingMinors.length" class="mb-4">
        <uw-card-status>
          <template #status-label>
            {{ pendingMinors.length > 1 ? 'Minors' : 'Minor' }}
            Beginning <br>
            {{ quarter }}
          </template>
          <template #status-value>
            <span
              v-for="(minor, i) in pendingMinors"
              :key="i"
              class="fw-bold"
            >
              {{ minor.abbr }}
            </span>
          </template>
        </uw-card-status>
      </div>

      <uw-myplan
        v-if="!myPlanPeakLoad && myPlanData !== null"
        :my-plan-data="myPlanData || {}"
        :year="year"
        :quarter="quarter"
      />

      <uw-resources
        :my-plan-data="myPlanData || {}"
        :registration-is-open="
          estRegData.noticeMyRegIsOpen ||
            (!estRegData.hasEstRegDataNotice && regPeriod1Started)
        "
        :next-term-year="year"
        :next-term-quarter="quarter"
        :pre-reg-notices="preRegNotices"
      />

      <uw-fin-aid
        v-if="finAidNotices && finAidNotices.length && isSummerReg"
        :fin-aid-notices="finAidNotices"
      />
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';

import Card from '../../_templates/card.vue';
import CardStatus from '../../_templates/card-status.vue';
import EstRegComponent from './est-reg-date.vue';
import HoldsComponent from './holds.vue';
import MyPlanComponent from './myplan.vue';
import ResourcesComponent from './resources.vue';
import FinAidComponent from '../../_common/finaid.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-card-status': CardStatus,
    'uw-est-reg-date': EstRegComponent,
    'uw-fin-aid': FinAidComponent,
    'uw-holds': HoldsComponent,
    'uw-myplan': MyPlanComponent,
    'uw-resources': ResourcesComponent,
  },
  props: {
    forQuarter: {
      type: String,   // optional value: Summer
      default: null,
    },
    period: {
      type: String,   // optional value: A
      default: null,
    },
  },
  data() {
    return {
      isOpen: false,
    };
  },
  computed: {
    ...mapState({
      student: (state) => state.user.affiliations.student,
      isAfterStartOfRegistrationDisplayPeriod: (state) =>
        state.cardDisplayDates.is_after_start_of_registration_display_period,
      isBeforeEndOfRegistrationDisplayPeriod: (state) =>
        state.cardDisplayDates.is_before_end_of_registration_display_period,
      isAfterStartOfSummerRegDisplayPeriodA: (state) =>
        state.cardDisplayDates.is_after_start_of_summer_reg_display_periodA,
      isAfterStartOfSummerRegDisplayPeriod1: (state) =>
        state.cardDisplayDates.is_after_start_of_summer_reg_display_period1,
      myPlanPeakLoad: (state) => state.cardDisplayDates.myplan_peak_load,
      regPeriod1Started: (state) => state.cardDisplayDates.reg_period1_started,
    }),
    ...mapState('notices', {
      notices: (state) => state.value,
    }),
    ...mapState('oquarter', {
      year: (state) => state.value.next_term_data.year,
      quarter(state) {
        if (this.forQuarter) {
          return this.forQuarter;
        }
        return state.value.next_term_data.quarter;
      },
      nextTermHasReg: (state) => state.value.next_term_data.has_registration,
      terms: (state) => state.value.terms,
    }),
    ...mapState('profile', {
      profile: (state) => state.value,
    }),
    ...mapState('myplan', {
      myPlanData: function(state) {
        return state.value[`${this.year}/${this.quarter}`];
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
    isSummerReg() {
      return this.forQuarter === 'Summer';
    },
    summerShouldDisplay() {
      return (
        this.isSummerReg &&
        ((this.period === 'A' && this.isAfterStartOfSummerRegDisplayPeriodA) ||
          (this.period === '1' && this.isAfterStartOfSummerRegDisplayPeriod1))
      );
    },
    shouldDisplayAtAll() {
      if (this.isSummerReg) {
        return this.summerShouldDisplay && this.student;
      }
      return (
        this.student &&
        this.isAfterStartOfRegistrationDisplayPeriod &&
        this.isBeforeEndOfRegistrationDisplayPeriod);
    },
    hasRegistration() {
      if (this.isQuarterReady) {
        if (this.isSummerReg) {
          return this.terms.some((term) => {
            // if any summer term has registration
            return (term.quarter === this.quarter && term.has_registration);
          });
        } else {
          return this.nextTermHasReg;
        }
      }
      return false;
    },
    hasDataToDisplay() {
      return (
        !this.hasRegistration &&
        // Can do any one of these
        ((this.finAidNotices && this.finAidNotices.length) ||
          this.estRegData.estRegDate ||
          (this.regHoldsNotices && this.regHoldsNotices.length) ||
          this.myPlanData)
      );
    },
    estRegDateNotices() {
      return this.notices.filter((notice) =>
        notice.location_tags.includes('est_reg_date'),
      );
    },
    preRegNotices() {
      return this.notices.filter((notice) =>
        notice.location_tags.includes('reg_card_messages'),
      );
    },
    regHoldsNotices() {
      return this.notices.filter((notice) =>
        notice.location_tags.includes('reg_card_holds'),
      );
    },
    finAidNotices() {
      return this.isSummerReg ?
        this.notices.filter((notice) =>
          notice.location_tags.includes('reg_summeraid_avail_title'),
        ) : [];
    },
    termMinors() {
      return this.profile.term_minors;
    },
    termMajors() {
      return this.profile.term_majors;
    },
    estRegData() {
      const estRegData = {};

      this.estRegDateNotices.forEach((notice) => {
        notice.attributes
            .filter((a) => a.name === 'Quarter' && a.value === this.quarter)
            .slice(0, 1)
            .forEach((a) => {
              estRegData.hasEstRegDataNotice = true;
              estRegData.noticeMyRegIsOpen = notice.my_reg_has_opened;
              estRegData.isMy1stRegDay = notice.is_my_1st_reg_day;
              estRegData.estRegDate = notice.dateStr;     // MUWM-5034
            });
      });

      return estRegData;
    },
    pendingMajors() {
      return this.retrieveQuarterDegrees(this.termMajors, 'majors');
    },
    pendingMinors() {
      return this.retrieveQuarterDegrees(this.termMinors, 'minors');
    },
    loaded() {
      let myPlanReady = true;
      if (
        this.isQuarterReady &&
        !this.hasRegistration &&
        (!this.isSummerReg || this.summerShouldDisplay)
      ) {
        myPlanReady =
          this.myPlanPeakLoad ||
          (!this.myPlanPeakLoad &&
            this.isMyPlanReadyTagged(`${this.year}/${this.quarter}`));
      }
      return (
        this.isNoticesReady &&
        this.isQuarterReady &&
        this.isProfileReady &&
        myPlanReady
      );
    },
    errored() {
      return (
        this.isNoticesErrored ||
        this.isQuarterErrored ||
        this.isProfileErrored ||
        (!this.myPlanPeakLoad &&
          this.isQuarterReady &&
          this.isMyPlanErroredTagged(`${this.year}/${this.quarter}`))
      );
    },
  },
  watch: {
    isQuarterReady: function(newValue, oldValue) {
      if (
        this.shouldDisplayAtAll &&
        !oldValue &&
        newValue &&
        !this.hasRegistration &&
        !this.myPlanPeakLoad &&
        (!this.isSummerReg || this.summerShouldDisplay)
      ) {
        this.fetchMyPlan({
          year: this.year,
          quarter: this.quarter,
        });
      }
    },
  },
  created() {
    if (this.shouldDisplayAtAll) {
      this.fetchNotices();
      this.fetchQuarters();
      this.fetchProfile();
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
      const filteredDegrees = degrees.filter(
          (degree) =>
            degree.quarter.toUpperCase() === this.quarter.toUpperCase() &&
          degree.year === this.year &&
          degree.degrees_modified &&
          !degree.has_only_dropped,
      );

      if (filteredDegrees && filteredDegrees.length) {
        return filteredDegrees[0][degreeType];
      } else {
        return [];
      }
    },
  },
};
</script>

<style lang="scss" scoped></style>
