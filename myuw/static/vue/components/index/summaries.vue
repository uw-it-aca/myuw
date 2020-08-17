<template>
  <b-row class="my-3">
    <b-col md="3">

      <a class="d-block border-bottom p-3 text-dark text-center" href="/academic_calendar/" v-if="termData">
        <i class="fa fa-calendar" aria-hidden="true"></i>
        <span v-if="termData.isBreak">
          <span v-if="termData.breakYear !== termData.year">
            {{ termData.year }} / {{ termData.breakYear }}
          </span>
          <span v-else>
            {{ termData.year }}
          </span>
        </span>
        <span v-else>
          {{ ucfirst(termData.quarter) }}
          {{ termData.year }}
        </span>
        <span v-if="termData.isFinal">Finals Week</span>
        <span v-else-if="termData.isBreak">
          {{ ucfirst(termData.breakQuarter) }}
          Break
        </span>
        <span v-else>
          Week {{ getWeeksApart(termData.firstDay, termData.todayDate) }} of
          {{ getWeeksApart(termData.firstDay, termData.lastDay ) }}
        </span>
      </a>

    </b-col>
    <b-col md="9" v-if="isHfsReady && isLibraryReady">

      <a class="d-inline-block border-left p-3 text-dark" href="/accounts/" v-if="hfs.student_husky_card">
        Student Husky<br>
        <span>${{ hfs.student_husky_card.balance.toFixed(2) }}</span>
      </a>
      <a class="d-inline-block border-left p-3 text-dark" href="/accounts/" v-if="hfs.resident_dining">
        Resident Dining<br>
        <span>${{ hfs.resident_dining.balance.toFixed(2) }}</span>
      </a>
      <a class="d-inline-block border-left p-3 text-dark"  href="/accounts/" v-if="hfs.employee_husky_card">
        Employee Husky<br>
        <span>${{ hfs.employee_husky_card.balance.toFixed(2) }}</span>
      </a>
      <a class="d-inline-block border-left p-3 text-dark"  href="/accounts/" v-if="library.next_due">
        Library Item Due<br>
        <span>{{ toFromNowDate(library.next_due) }}</span>
      </a>
      <a class="d-inline-block border-left p-3 text-dark" 
        href="https://search.lib.uw.edu/account"
        target="_blank" data-linklabel="Library Account Requests"
        v-else-if="library.holds_ready"
      >
        Library {{ library.holds_ready === 1 ? "Items" : "Item" }} Ready<br>
        <span>
          {{ library.holds_ready }}
          {{ library.holds_ready === 1 ? "Items" : "Item" }} ready
        </span>
      </a>
    </b-col>
  </b-row>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import moment from 'moment';

export default {
  data: function() {
    return {};
  },
  computed: {
    ...mapState({
      termData: (state) => state.termData,
    }),
    ...mapState('hfs', {
      hfs: (state) => state.value,
    }),
    ...mapState('library', {
      library: (state) => state.value,
    }),
    ...mapGetters('hfs', {
      isHfsReady: 'isReady',
      isHfsErrored: 'isErrored',
    }),
    ...mapGetters('library', {
      isLibraryReady: 'isReady',
      isLibraryErrored: 'isErrored',
    }),
  },
  mounted() {
    this.fetchHfs();
    this.fetchLibrary();
  },
  methods: {
    ...mapActions('hfs', {
      fetchHfs: 'fetch',
    }),
    ...mapActions('library', {
      fetchLibrary: 'fetch',
    }),
    getWeeksApart(qsDate, testDate) {
      const days = moment(testDate).diff(
          moment(qsDate).startOf('week'), 'days',
      );
      if (days < 0) {
        return 0;
      } else {
        return parseInt(days / 7) + 1;
      }
    },
    ucfirst: (s) => s.replace(/^([a-z])/, (c) => c.toUpperCase()),
    toFromNowDate: (s) => moment(s).fromNow(),
  },
};
</script>

<style lang="scss" scoped></style>
