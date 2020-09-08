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
      <b-tabs v-model="tabIndex" pills justified
              nav-class="mb-4"
              active-nav-item-class="bg-beige text-body font-weight-bold"
      >
        <b-tab v-for="(period, i) in periods" :key="i" :title="period.title"
               title-item-class="bg-light text-nowrap text-uppercase
               myuw-text-xs mr-1 mb-1"
               title-link-class="text-body h-100"
               :active="(
                 period.start_date <= today &&
                 period.end_date >= today
               ) || (
                 i > 0 &&
                 periods[i - 1].end_date < today &&
                 period.title === 'finals'
               )"
        >
          <!-- tab content -->
          <uw-schedule-tab :period="period" />
        </b-tab>
      </b-tabs>
      <!-- TODO: commented till functionality is confirmed,
      this can go into the "card notification header" -->
      <!-- <p v-if="offTerm.length > 0">
        Note:
        <span v-for="(term, i) in offTerm" :key="i">
          {{term.section}} course continues until {{formatTime(term.end_date)}}
        </span>
      </p> -->
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
    ...mapGetters('schedule', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
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
  },
  mounted() {
    if (this.term) this.fetch(this.term);
  },
  methods: {
    ...mapActions('schedule', ['fetch']),
    // TODO: move every instance of this functions into global scope
    ucfirst: (s) => s.replace(/^([a-z])/, (c) => c.toUpperCase()),
    formatDate: (d) => {
      return d.format('MMM D');
    },
    formatTime: (t) => {
      return t.format('h:mmA');
    },
  },
};
</script>
