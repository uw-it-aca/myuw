<template>
  <uw-card
    v-if="!isErrored && term && (!isReady || periods.length > 0)"
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
      <div v-if="periods[tabIndex].eosData.length > 0">
        <span v-for="(eosSection, i) in periods[tabIndex].eosData" :key="i">
          <h4>
            {{eosSection.curriculum_abbr}} {{eosSection.course_number}}
            {{eosSection.section_id}} meeting times:&nbsp;
          </h4>
          <ol>
            <li v-for="(meeting, i) in eosSection.meetings" :key="i">
              <span v-if="i !== 0">,&nbsp;</span>
              <span v-if="meeting.eos_start_date">
                {{formatDate(meeting.eos_start_date)}}
                <span v-if="!meeting.start_end_same">
                  &ndash; {{formatDate(meeting.eos_end_date)}}
                </span>
              </span>
              <span v-if="meeting.wont_meet">
                (Class does not meet)
              </span>
              <span v-else-if="meeting.no_meeting">
                (Online learning)
              </span>
              <span v-else>
                <span v-if="meeting.start_time">
                  ({{formatTime(meeting.start_time)}} &ndash;
                  {{formatTime(meeting.end_time)}})
                </span>
              </span>
            </li>
          </ol>
        </span>
      </div>
      <b-tabs v-model="tabIndex">
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
      tabIndex: 0,
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
    formatDate: (d) => {
      return d.format("MMM D");
    },
    formatTime: (t) => {
      return t.format("h:mmA");
    }
  },
}
</script>