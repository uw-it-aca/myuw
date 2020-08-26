<template>
  <b-row class="mb-3" :class="[$mq == 'tablet' ? 'mt-3' : '']"
         role="group" aria-labelledby="summaryHeader"
  >
    <h3 id="summaryHeader" class="sr-only">
      Account Summaries
    </h3>
    <b-col md="2">
      <a
        v-if="termData"
        class="d-block px-3 py-2 text-dark text-nowrap font-weight-light myuw-text-sm"
        :class="[
          $mq == 'tablet' || $mq == 'desktop'
            ? 'border-left text-left'
            : 'border-bottom text-center',
        ]"
        href="/academic_calendar/"
      >
        <font-awesome-icon :icon="['far', 'calendar-alt']" />
        <span v-if="termData.isBreak">
          <span v-if="termData.breakYear !== termData.year">
            {{ termData.year }} / {{ termData.breakYear }}
          </span>
          <span v-else>{{ termData.year }}</span>
        </span>
        <span v-else>
          {{ ucfirst(termData.quarter) }}
          {{ termData.year }}
        </span>
        <strong v-if="termData.isFinal"
                class="text-dark d-block font-weight-bold myuw-text-md"
        >Finals Week</strong>
        <strong
          v-else-if="termData.isBreak"
          class="text-dark d-block font-weight-bold myuw-text-md"
        >
          {{ ucfirst(termData.breakQuarter) }}
          Break
        </strong>
        <strong v-else class="text-dark d-block font-weight-bold myuw-text-md">
          Week {{ getWeeksApart(termData.firstDay, termData.todayDate) }} of
          {{ getWeeksApart(termData.firstDay, termData.lastDay) }}
        </strong>
      </a>
    </b-col>
    <b-col v-if="isHfsReady && isLibraryReady" md="10">
      <div class="row float-md-right">
        <a
          v-if="hfs.student_husky_card"
          class="d-inline-block col px-3 py-2 font-weight-light text-dark text-nowrap
          myuw-text-sm"
          :class="[
            $mq == 'tablet' || $mq == 'desktop'
              ? 'border-left text-left myuw-min-width-25'
              : 'border-none text-center',
          ]"
          href="/accounts/"
        >
          Student Husky
          <strong class="text-dark d-block font-weight-bold myuw-text-md">
            ${{ hfs.student_husky_card.balance.toFixed(2) }}
          </strong>
        </a>
        <a
          v-if="hfs.resident_dining"
          class="d-inline-block col px-3 py-2 font-weight-light text-dark text-nowrap
          myuw-text-sm"
          :class="[
            $mq == 'tablet' || $mq == 'desktop'
              ? 'border-left text-left myuw-min-width-25'
              : 'border-none text-center',
          ]"
          href="/accounts/"
        >
          Resident Dining
          <strong class="text-dark d-block font-weight-bold myuw-text-md">
            ${{ hfs.resident_dining.balance.toFixed(2) }}
          </strong>
        </a>

        <a
          v-if="hfs.employee_husky_card"
          class="d-inline-block col px-3 py-2 font-weight-light text-dark text-nowrap
          myuw-text-sm"
          :class="[
            $mq == 'tablet' || $mq == 'desktop'
              ? 'border-left text-left myuw-min-width-25'
              : 'border-none text-center',
          ]"
          href="/accounts/"
        >
          Employee Husky
          <strong class="text-dark d-block font-weight-bold myuw-text-md">
            ${{ hfs.employee_husky_card.balance.toFixed(2) }}
          </strong>
        </a>
        <a
          v-if="library.next_due"
          class="d-inline-block col px-3 py-2 font-weight-light text-dark text-nowrap
          myuw-text-sm"
          :class="[
            $mq == 'tablet' || $mq == 'desktop'
              ? 'border-left text-left myuw-min-width-25'
              : 'border-none text-center',
          ]"
          href="/accounts/"
        >
          Library Item Due
          <strong class="text-dark d-block font-weight-bold myuw-text-md">
            {{ toFromNowDate(library.next_due) }}
          </strong>
        </a>
        <a
          v-else-if="library.holds_ready"
          class="d-inline-block col px-3 py-2 font-weight-light text-dark text-nowrap
          myuw-text-sm"
          :class="[
            $mq == 'tablet' || $mq == 'desktop'
              ? 'border-left text-left myuw-min-width-25'
              : 'border-none text-center',
          ]"
          href="https://search.lib.uw.edu/account"
          target="_blank"
          aria-label="Library Account Requests"
        >
          Library {{ library.holds_ready === 1 ? 'Items' : 'Item' }} Ready
          <strong class="text-dark d-block font-weight-bold myuw-text-md">
            {{ library.holds_ready }}
            {{ library.holds_ready === 1 ? 'Items' : 'Item' }} ready
          </strong>
        </a>
      </div>
    </b-col>
  </b-row>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import moment from 'moment';

export default {
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
          moment(qsDate).startOf('week'),
          'days',
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

<style lang="scss" scoped>
.myuw-min-width-25 {
  min-width: 25%;
}
</style>
