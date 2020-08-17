<template>
  <b-row>
    <b-col>
      <a
        v-if="termData"
        href="/academic_calendar/"
      >
        <i
          class="fa fa-calendar"
          aria-hidden="true"
        />
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
    <b-col v-if="isHfsReady && isLibraryReady">
      <a
        v-if="hfs.student_husky_card"
        href="/accounts/"
      >
        Student Husky
        <span>${{ hfs.student_husky_card.balance.toFixed(2) }}</span>
      </a>
      <a
        v-if="hfs.resident_dining"
        href="/accounts/"
      >
        Resident Dining
        <span>${{ hfs.resident_dining.balance.toFixed(2) }}</span>
      </a>
      <a
        v-if="hfs.employee_husky_card"
        href="/accounts/"
      >
        Employee Husky
        <span>${{ hfs.employee_husky_card.balance.toFixed(2) }}</span>
      </a>
      <a
        v-if="library.next_due"
        href="/accounts/"
      >
        Library Item Due
        <span>{{ toFromNowDate(library.next_due) }}</span>
      </a>
      <a
        v-else-if="library.holds_ready"
        href="https://search.lib.uw.edu/account"
        target="_blank"
        data-linklabel="Library Account Requests"
      >
        Library {{ library.holds_ready === 1 ? "Items" : "Item" }} Ready
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
