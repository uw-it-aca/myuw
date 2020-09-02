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
      <div v-if="periods[tabIndex].eosData.length > 0">
        <span v-for="(eosSection, i) in periods[tabIndex].eosData" :key="i">
          <h4>
            {{ eosSection.curriculum_abbr }} {{ eosSection.course_number }}
            {{ eosSection.section_id }} meeting times:&nbsp;
          </h4>
          <ol>
            <li v-for="(meeting, j) in eosSection.meetings" :key="j">
              <span v-if="i !== 0">,&nbsp;</span>
              <span v-if="meeting.eos_start_date">
                {{ formatDate(meeting.eos_start_date) }}
                <span v-if="!meeting.start_end_same">
                  &ndash; {{ formatDate(meeting.eos_end_date) }}
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
                  ({{ formatTime(meeting.start_time) }} &ndash;
                  {{ formatTime(meeting.end_time) }})
                </span>
              </span>
            </li>
          </ol>
        </span>
      </div>

      <b-tabs v-model="tabIndex" pills
              nav-class="mt-4 mb-1"
              active-nav-item-class="bg-light text-body font-weight-bold"
      >
        <b-tab v-for="(period, i) in periods" :key="i" :title="period.title"
               title-item-class="text-uppercase myuw-text-xs mr-1"
               title-link-class="text-dark"
               :active="i == 0"
        >
          <uw-schedule-tab :period="period" />
        </b-tab>
      </b-tabs>
      <!-- commented till functionality is confirmed -->
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
