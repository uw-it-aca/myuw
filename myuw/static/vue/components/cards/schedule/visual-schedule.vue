<template>
  <uw-card
    v-if="!isErrored && term && (!isReady || periods.length > 0)"
    :loaded="isReady" :errored="isErrored"
  >
    <template #card-heading>
      <h3 class="text-dark-beige">
        {{ termName }} Schedule
        <span class="sr-only">
          Final exam schedule and Visual Schedule
        </span>
      </h3>
    </template>

    <template #card-body>
      <!-- schedule tabs -->
      <b-tabs v-model="tabIndex" pills
              nav-wrapper-class="mb-3 p-1"
              nav-class=""
              active-nav-item-class="bg-beige text-body font-weight-bold"
      >
        <b-tab v-for="(period, i) in periods" :key="i" :title="period.title"
               title-item-class="bg-light text-nowrap text-uppercase
               myuw-text-xs mr-1 mb-1"
               title-link-class="text-body h-100"
               :active="period.id == activePeriod.id"
        >
          <!-- tab content -->
          <uw-schedule-tab :period="period" />
        </b-tab>
      </b-tabs>
      <!-- TODO: charlon style this, use billpce on 2019-06-26 to test it -->
      <p v-if="offTerm.length > 0">
        Note:
        <span v-for="(termData, i) in offTerm" :key="i">
          {{ termData.section }} course continues until
          {{ formatDate(termData.end_date) }}
        </span>
      </p>
    </template>
  </uw-card>
</template>

<script>
import moment from 'moment';
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../../containers/card.vue';
import ScheduleTab from './schedule-tab.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-schedule-tab': ScheduleTab,
  },
  data: function() {
    return {
      term: 'current',
      tabIndex: 0,
    };
  },
  computed: {
    ...mapState({
      allSchedules: (state) => state.schedule.value,
      today: (state) => moment(state.termData.today, 'dddd, MMMM D, YYYY'),
    }),
    ...mapGetters('schedule', [
      'isReadyTagged',
      'isErroredTagged',
    ]),
    isReady() {
      return this.isReadyTagged(this.term);
    },
    isErrored() {
      return this.isErroredTagged(this.term);
    },
    offTerm: function() {
      return this.allSchedules[this.term].off_term_trimmed;
    },
    periods: function() {
      return this.allSchedules[this.term].periods;
    },
    termName: function() {
      const termData = this.allSchedules[this.term].term;
      let name = this.ucfirst(termData.quarter) + ' ' + termData.year;
      if (termData.summer_term) {
        name += ' ' + termData.summer_term.split('-')
            .map(this.ucfirst).join('-');
      }
      return name;
    },
    activePeriod: function() {
      for (const i in Object.keys(this.periods)) {
        if (
          !this.periods[i].end_date ||
          this.periods[i].end_date >= this.today
        ) {
          return this.periods[i];
        }
      }
      return this.periods[Object.keys(this.periods)[this.periods.length - 1]];
    },
  },
  mounted() {
    if (this.term) this.fetch(this.term);
  },
  methods: {
    ...mapActions('schedule', ['fetch']),
    // TODO: move every instance of this functions into global scope
    ucfirst: (s) => s.replace(/^([a-z])/, (c) => c.toUpperCase()),
    formatDate: (t) => {
      return moment(t).format('ddd, MMM D');
    },
  },
};
</script>
