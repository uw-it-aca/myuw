<template>
  <b-row>
    <b-col>
      <a href="/academic_calendar/" v-if="termData">
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
          {{ getWeeksApart(termData.firstDay, termData.lastDay )}}
        </span>
      </a>
    </b-col>
    <b-col v-if="isHfsReady && isLibraryReady">
      <a href="/accounts/" v-if="hfs.student_husky_card">
        Student Husky
        <span>${{ hfs.student_husky_card.balance.toFixed(2) }}</span>
      </a>
      <a href="/accounts/" v-if="hfs.resident_dining">
        Resident Dining
        <span>${{ hfs.resident_dining.balance.toFixed(2) }}</span>
      </a>
      <a href="/accounts/" v-if="hfs.employee_husky_card">
        Employee Husky
        <span>${{ hfs.employee_husky_card.balance.toFixed(2) }}</span>
      </a>
      <a href="/accounts/" v-if="library.next_due">
        Library Item Due
        <span>{{ toFromNowDate(library.next_due) }}</span>
      </a>
      <a
        href="https://search.lib.uw.edu/account"
        target="_blank" data-linklabel="Library Account Requests"
        v-else-if="library.holds_ready"
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
import { mapGetters, mapState, mapActions } from "vuex";
import moment from 'moment';

export default {
  data: function () {
    return {};
  },
  computed: {
    ...mapState({
      termData: (state) => state.termData,
    }),
    ...mapState("hfs", {
      hfs: (state) => state.value,
    }),
    ...mapState("library", {
      library: (state) => state.value,
    }),
    ...mapGetters("hfs", {
      isHfsReady: "isReady",
      isHfsErrored: "isErrored",
    }),
    ...mapGetters("library", {
      isLibraryReady: "isReady",
      isLibraryErrored: "isErrored",
    }),
  },
  methods: {
    ...mapActions("hfs", {
      fetchHfs: "fetch",
    }),
    ...mapActions("library", {
      fetchLibrary: "fetch",
    }),
    getWeeksApart(qs_date, test_date) {
      // qs_date: quarter start date
      var one_day_ms = 24 * 3600 * 1000;
      var one_week_ms = one_day_ms * 7;
      var t1 = qs_date.getTime(); // milliseconds since January 1, 1970
      var qs_day_of_week = qs_date.getDay();
      var qs_prev_sunday = t1 - (one_day_ms * qs_day_of_week);
      var t2 = test_date.getTime();
      if (t2 < qs_prev_sunday) {
        return 0;
      } else {
        return parseInt((t2 - qs_prev_sunday) / one_week_ms) + 1;
      }
    },
    ucfirst: (s) => s.replace(/^([a-z])/, (c) => c.toUpperCase()),
    toFromNowDate: (s) => moment(s).fromNow(),
  },
  created() {
    this.fetchHfs();
    this.fetchLibrary();
  }
};
</script>

<style lang="scss" scoped></style>
