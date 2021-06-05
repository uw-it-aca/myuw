<template>
  <uw-card
    v-if="!isErrored && termLabel && (!isReady || periods.length > 0)"
    :loaded="isReady" :errored="isErrored"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        {{ termName }} Schedule
        <span class="sr-only">
          Final exam schedule and Visual Schedule
        </span>
      </h2>
    </template>

    <template #card-body>
      <div>
      <!-- schedule tabs -->
      <b-tabs v-if="!allSchedules[termLabel].noPeriodsNoMeetings"
              v-model="tabIndex" pills
              nav-wrapper-class="mb-3 p-0"
              active-nav-item-class="bg-transparent rounded-0
              myuw-border-bottom border-dark text-body font-weight-bold"
      >
        <b-tab v-for="(period, i) in periods" :key="i" :title="period.title"
               title-item-class="text-nowrap text-uppercase
               myuw-text-xs mr-2 mb-1"
               title-link-class="rounded-0 px-2 py-1 h-100
               text-body myuw-border-bottom"
               :active="period.id == activePeriod.id"
        >
          <!-- tab content -->
          <uw-schedule-tab
            :period="period"
            :term="allSchedules[termLabel].term"
          />
        </b-tab>
      </b-tabs>

      <div v-else>
        <p class="text-muted myuw-text-md mb-1">
          No meeting time specified:
        </p>
        <div v-for="(meeting, i) in allMeetings" :key="i"
            class="d-inline-block w-auto mr-2"
            style="min-width:110px;"
        >
          <uw-course-section
            :meeting-data="meeting"
            :term="allSchedules[termLabel].term"
          />
        </div>
      </div>

      <!-- TODO: charlon style this, use billpce on 2019-06-26 to test it -->
      <p v-if="offTerm.length > 0" class="m-0 text-muted myuw-text-md">
        Note:
        <span v-for="(termData, i) in offTerm" :key="i">
          {{ termData.section }} course continues until
          {{ formatDate(termData.end_date) }}
        </span>
      </p>
      </div>
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';
import ScheduleTab from './schedule-tab.vue';
import CourseSection from './course-section.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-schedule-tab': ScheduleTab,
    'uw-course-section': CourseSection,
  },
  props: {
    termLabel: {
      type: String,
      default: 'current',
    },
  },
  data: function() {
    return {
      tabIndex: 0,
    };
  },
  computed: {
    ...mapState({
      allSchedules: (state) => state.visual_schedule.value,
    }),
    ...mapGetters('visual_schedule', [
      'isReadyTagged',
      'isErroredTagged',
    ]),
    isReady() {
      return this.isReadyTagged(this.termLabel);
    },
    isErrored() {
      return this.isErroredTagged(this.termLabel);
    },
    offTerm: function() {
      return this.allSchedules[this.termLabel].off_term_trimmed;
    },
    periods: function() {
      return this.allSchedules[this.termLabel].periods;
    },
    termName: function() {
      const termData = this.allSchedules[this.termLabel].term;
      let name = this.titleCaseWord(termData.quarter) + ' ' + termData.year;
      if (termData.summer_term) {
        name += ' ' + this.capitalizeString(termData.summer_term);
      }
      return name;
    },
    activePeriod: function() {
      for (const i in Object.keys(this.periods)) {
        if (
          !this.periods[i].end_date ||
          this.periods[i].end_date >= this.nowDatetime().clone().hour(0).minute(0)
        ) {
          return this.periods[i];
        }
      }
      return this.periods[Object.keys(this.periods)[this.periods.length - 1]];
    },
    allMeetings() {
      return this.allSchedules[this.termLabel]
        .periods
        .flatMap((period) => period.sections)
        .flatMap((section) => section.meetings.map((meeting) => {
          return { section, meeting };
        }));
    }
  },
  mounted() {
    if (this.termLabel) this.fetch(this.termLabel);
  },
  methods: {
    ...mapActions('visual_schedule', ['fetch']),
    formatDate(t) {
      return this.dayjs(t).format('ddd, MMM D');
    },
  },
};
</script>
