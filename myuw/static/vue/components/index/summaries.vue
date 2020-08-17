<template>
  <b-row class="myuw-account-summaries mb-3">
    <b-col md="4">
      <a
        v-if="termData"
        class="d-block px-3 pb-2 text-dark text-nowrap"
        v-bind:class="[$mq == 'tablet' || $mq=='desktop' ? 'border-left text-left' : 'border-bottom text-center']"
        href="/academic_calendar/"
      >
        <font-awesome-icon :icon="['far', 'calendar-alt']" />
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
        <strong v-else>
          Week {{ getWeeksApart(termData.firstDay, termData.todayDate) }} of
          {{ getWeeksApart(termData.firstDay, termData.lastDay) }}
        </strong>
      </a>
    </b-col>
    <b-col md="8" v-if="isHfsReady && isLibraryReady">
      
      <div class="row">
      <a
        class="d-inline-block col-6 col-sm-3 px-3 text-dark text-nowrap"
        v-bind:class="[$mq == 'tablet' || $mq=='desktop' ? 'border-left text-left pb-2' : 'py-2 border-none text-center']"
        href="/accounts/"
        v-if="hfs.student_husky_card"
      >
        Student Husky
        <strong>${{ hfs.student_husky_card.balance.toFixed(2) }}</strong>
      </a>
      <a
        class="d-inline-block col-6 col-sm-3 px-3 text-dark text-nowrap"
        v-bind:class="[$mq == 'tablet' || $mq=='desktop' ? 'border-left text-left pb-2' : 'py-2 border-none text-center']"
        href="/accounts/"
        v-if="hfs.resident_dining"
      >
        Resident Dining
        <strong>${{ hfs.resident_dining.balance.toFixed(2) }}</strong>
      </a>

      <a
        class="d-inline-block col-6 col-sm-3 px-3 text-dark text-nowrap"
        v-bind:class="[$mq == 'tablet' || $mq=='desktop' ? 'border-left text-left pb-2' : 'py-2 border-none text-center']"
        href="/accounts/"
        v-if="hfs.employee_husky_card"
      >
        Employee Husky
        <strong>${{ hfs.employee_husky_card.balance.toFixed(2) }}</strong>
      </a>
      <a
        class="d-inline-block col-6 col-sm-3 px-3 text-dark text-nowrap"
        v-bind:class="[$mq == 'tablet' || $mq=='desktop' ? 'border-left text-left pb-2' : 'py-2 border-none text-center']"
        href="/accounts/"
        v-if="library.next_due"
      >
        Library Item Due
        <strong>{{ toFromNowDate(library.next_due) }}</strong>
      </a>
      <a
        class="d-inline-block col-6 col-sm-3 px-3 text-dark text-nowrap"
        v-bind:class="[$mq == 'tablet' || $mq=='desktop' ? 'border-left text-left pb-2' : 'py-2 border-none text-center']"
        href="https://search.lib.uw.edu/account"
        target="_blank"
        data-linklabel="Library Account Requests"
        v-else-if="library.holds_ready"
      >
        Library {{ library.holds_ready === 1 ? 'Items' : 'Item' }} Ready
        <strong>
          {{ library.holds_ready }}
          {{ library.holds_ready === 1 ? 'Items' : 'Item' }} ready
        </strong>
      </a>
      </div>
    </b-col>
  </b-row>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex';
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

<style lang="scss" scoped>
  .myuw-account-summaries {
    font-size: 0.85rem;

    strong {
      font-size: 0.95rem;
      display: block;
    }
  }
</style>
