<template>
  <uw-card v-if="shouldDisplayAtAll"
           :loaded="loaded" :errored="errored"
  >
    <template #card-heading>
      <h3>
        Registration: {{quarter}} {{year}}
      </h3>
    </template>
    <template #card-body>
      <uw-est-reg-date :estRegData="estRegData"/>
      <uw-holds
        v-if="regHoldsNotices && regHoldsNotices.length"
        :myPlanData="myPlanData"
        :regHoldsNotices="regHoldsNotices"
      />

      <div>
        <h4 v-if="pendingMajors.length">
          {{pendingMajors.length > 1 ? "Majors" : "Major"}}
          Beginning <br>
          {{quarter}}
        </h4>
        <span v-for="(major, i) in pendingMajors" :key="i">
          {{major.degree_abbr}}
        </span>
      </div>

      <div>
        <h4 v-if="pendingMinors.length">
          {{pendingMinors.length > 1 ? "Minors" : "Minor"}}
          Beginning <br>
          {{quarter}}
        </h4>
        <span v-for="(minor, i) in pendingMinors" :key="i">
          {{minor.abbr}}
        </span>
      </div>

      <uw-in-myplan
        v-if="myPlanData"
        :myPlanData="myPlanData"
        :quarter="quarter"
      />

      <span v-if="estRegData.estRegDate && estRegData.isMy1stRegDay">
        Registration opens at 6:00AM
      </span>

      <uw-resources
        :myPlanData="myPlanData"
        :registrationIsOpen="estRegData.noticeMyRegIsOpen || (
          !estRegData.hasEstRegDataNotice &&
          regPeriod1Started
        )"
        :nextTermYear="year"
        :nextTermQuarter="quarter"
        :preRegNotices="preRegNotices"
      />

      <uw-fin-aid 
        v-if="finAidNotices && finAidNotices.length && isSummerReg"
        :finAidNotices="finAidNotices"
      />
    </template>
    <template v-if="myPlanData" #card-disclosure>
      <b-collapse id="myplan-courses-collapse" v-model="isOpen">
        <uw-myplan-courses
          :nextTermYear="year"
          :nextTermQuarter="quarter"
          :myPlanData="myPlanData"
        />
      </b-collapse>
    </template>
    <template v-if="myPlanData" #card-footer>
      <b-button
        v-if="!isOpen"
        v-b-toggle.myplan-courses-collapse
        :aria-label="
          `Expand to show your ${quarter} ${year} plan`
        "
        variant="link"
        size="sm"
        class="w-100 p-0 text-dark"
      >
        <!-- TODO: @charlon add a css capital class for this button -->
        SHOW {{quarter}} {{year}} PLAN
      </b-button>
      <b-button
        v-else
        v-b-toggle.myplan-courses-collapse
        :aria-label="
          `Collapse to hide your ${quarter} ${year} plan`
        "
        variant="link"
        size="sm"
        class="w-100 p-0 text-dark"
      >
        <!-- TODO: @charlon add a css capital class for this button -->
        HIDE {{quarter}} {{year}} PLAN
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
  props: {
    quarter: {
      type: String,
      default: "",
    },
    year: {
      type: Number,
      default: -1,
    },
    oquarterData: {
      type: Object,
      default: null,
    },
    myPlanData: {
      type: Object,
      default: null,
    },
    loaded: {
      type: Boolean,
      required: true,
    },
    errored: {
      type: Boolean,
      required: true,
    },
    notices: {
      type: Array,
      default: [],
    },
    profile: {
      type: Object,
      default: {},
    },
  },
  computed: {
    ...mapState({
      student: (state) => state.user.affiliations.student,
      seattle: (state) => state.user.affiliations.seattle,
      bothell: (state) => state.user.affiliations.bothell,
      tacoma: (state) => state.user.affiliations.tacoma,
      regPeriod1Started: (state) => state.cardDisplayDates.reg_period1_started,
    }),
    estRegDateNotices() {
      return this.notices.filter(
        (notice) => notice.location_tags.includes('est_reg_date'),
      );
    },
    preRegNotices() {
      return this.notices.filter(
        (notice) => notice.location_tags.includes('reg_card_messages'),
      );
    },
    regHoldsNotices() {
      return this.notices.filter(
        (notice) => notice.location_tags.includes('reg_card_holds'),
      );
    },
    finAidNotices() {
      return this.isSummerReg ? this.notices.filter(
        (notice) => notice.location_tags.includes('reg_summeraid_avail_title'),
      ) : [];
    },
    termMinors() {return this.profile.term_minors},
    termMajors() {return this.profile.term_majors},
    shouldDisplayAtAll: function() {
      if (this.loaded) {
        return !(this.isSummerReg && this.hasRegistration) && (
          // Can do any one of these
          (this.finAidNotices && this.finAidNotices.length) ||
          this.estRegData.estRegDate ||
          (this.regHoldsNotices && this.regHoldsNotices.length) ||
          this.myPlanData
        )
      }

      return false;
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
            a.value === this.quarter
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
      return this.quarter === "Summer";
    },
    hasRegistration() {
      if (this.oquarterData) {
        if (this.isSummerReg) {
          let hasReg = false;
          this.oquarterData.terms.forEach((term) => {
            if (term.quarter === this.quarter && term.section_count) {
              hasReg = true;
            }
          });
          return hasReg;
        } else {
          return this.oquarterData.next_term_data.has_registration;
        }
      }
      return false;
    },
  },
  data() {
    return {
      isOpen: false,
    }
  },
  methods: {
    retrieveQuarterDegrees(degrees, degreeType) {
      let filteredDegrees = degrees.filter((degree) => (
        degree.quarter.toUpperCase() === this.quarter.toUpperCase() &&
        degree.year === this.year &&
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