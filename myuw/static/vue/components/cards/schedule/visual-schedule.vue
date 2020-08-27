<template>
  <uw-card
    v-if="term && (!isReady || periods.length > 0)"
    :loaded="isReady" :errored="isErrored"
  >
    <template #card-heading>
      <h3>
        {{termName}} Schedule
        <span class="sr-only">
          Final exam schedule and Visual Schedule
        </span>
      </h3>
    </template>
    <template #card-body>
      <!-- TODO: add the eos disclaimer
      https://github.com/uw-it-aca/myuw/blob/5fc7c436d50f3050991f25d4c1a873e4005536ea/myuw/templates/handlebars/card/schedule/visual.html#L11-L20
      -->
      <h4 class="sr-only">{{termName}} Final Exam Schedule</h4>
      <b-tabs>
        <uw-schedule-tab
          v-for="(period, i) in periods" :key="i" :title="period.title"
          :active="i == 0" :period="period"
        />
      </b-tabs>
    </template>
  </uw-card>
</template>

<script>
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
    };
  },
  computed: {
    ...mapState({
      allSchedules: (state) => state.schedule.value,
    }),
    ...mapGetters('schedule', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
    offTerm: function() {
      return this.allSchedules[this.term].off_term_trimmed;
    },
    periods: function() {return this.allSchedules[this.term].periods;},
    termName: function() {
      let termData = this.allSchedules[this.term].term;
      let name = this.ucfirst(termData.quarter) + " " + termData.year;
      if (termData.summer_term) {
        name += " " + termData.summer_term.split('-').map(ucfirst).join('-');
      }
      return name;
    }
  },
  mounted() {
    if (this.term) this.fetch(this.term);
  },
  methods: {
    ...mapActions('schedule', ['fetch']),
    // TODO: move every instance of this functions into global scope
    ucfirst: (s) => s.replace(/^([a-z])/, (c) => c.toUpperCase()),
  },
}
</script>