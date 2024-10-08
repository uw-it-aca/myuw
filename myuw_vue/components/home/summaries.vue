<template>
  <div class="row mb-3"
         role="group" aria-labelledby="summaryHeader"
  >
    <h2 id="summaryHeader" class="visually-hidden">
      Account Summaries
    </h2>
    <div class="col-md-2">
      <a
        v-if="termData"
        v-inner="'MyUW Calendar page'"
        class="d-block px-3 py-1 text-dark text-nowrap
        fw-light"
        :class="[
          $mq == 'tablet' || $mq == 'desktop'
            ? 'border-start text-start'
            : 'border-bottom text-center',
        ]"
        href="/academic_calendar/"
      >
        <span class="d-inline-block bg-light myuw-text-sm">
          <font-awesome-icon :icon="faCalendarAlt" />
          <span v-if="termData.isBreak">
            <span v-if="termData.breakYear !== termData.year">
              {{ termData.year }} / {{ termData.breakYear }}
            </span>
            <span v-else>{{ termData.year }}</span>
          </span>
          <span v-else>
            {{ titleCaseWord(termData.quarter) }}
            {{ termData.year }}
          </span>
        </span>
        <span v-if="termData.isFinals"
              class="text-dark d-block fw-bold"
        >Finals Week</span>
        <span
          v-else-if="termData.isBreak"
          class="text-dark d-block fw-bold"
        >
          {{ titleCaseWord(termData.breakQuarter) }}
          Break
        </span>
        <span v-else class="text-dark d-block fw-bold">
          Week {{ getWeeksApart(termData.firstDay, termData.todayDate) }} of
          {{ getWeeksApart(termData.firstDay, termData.lastDay) }}
        </span>
      </a>
    </div>
    <div v-if="loadData && (isHfsReady || isLibraryReady)" class="col-md-10">
      <div class="row float-md-end" style="padding: 0 10px;">
        <a
          v-if="hfs && hfs.student_husky_card"
          v-inner="'MyUW Accounts page - Student Husky card'"
          class="d-inline-block col px-3 py-1 ms-1
          fw-light text-dark text-nowrap"
          :class="[
            $mq == 'tablet' || $mq == 'desktop'
              ? 'border-start text-start'
              : 'border-none text-center',
          ]"
          href="/accounts/"
        >
          <span class="d-inline-block bg-light myuw-text-sm">
            Student Husky</span>
          <span class="text-dark d-block fw-bold">
            ${{ hfs.student_husky_card.balance.toFixed(2) }}
          </span>
        </a>
        <a
          v-if="hfs && hfs.resident_dining"
          v-inner="'MyUW Accounts page - Resident Dining'"
          class="d-inline-block col px-3 py-1 ms-1
          fw-light text-dark text-nowrap"
          :class="[
            $mq == 'tablet' || $mq == 'desktop'
              ? 'border-start text-start'
              : 'border-none text-center',
          ]"
          href="/accounts/"
        >
          <span class="d-inline-block bg-light myuw-text-sm">
            Resident Dining</span>
          <span class="text-dark d-block fw-bold">
            ${{ hfs.resident_dining.balance.toFixed(2) }}
          </span>
        </a>

        <a
          v-if="hfs && hfs.employee_husky_card"
          v-inner="'MyUW Accounts page - Employee Husky card'"
          class="d-inline-block col px-3 py-1 ms-1
          fw-light text-dark text-nowrap"
          :class="[
            $mq == 'tablet' || $mq == 'desktop'
              ? 'border-start text-start'
              : 'border-none text-center',
          ]"
          href="/accounts/"
        >
          <span class="d-inline-block bg-light myuw-text-sm">
            Employee Husky</span>
          <span class="text-dark d-block fw-bold">
            ${{ hfs.employee_husky_card.balance.toFixed(2) }}
          </span>
        </a>
        <a
          v-if="library && library.next_due"
          v-inner="'MyUW Accounts page - Library Account'"
          class="d-inline-block col px-3 py-1 ms-1
          fw-light text-dark text-nowrap"
          :class="[
            $mq == 'tablet' || $mq == 'desktop'
              ? 'border-start text-start'
              : 'border-none text-center',
          ]"
          href="/accounts/"
        >
          <span class="d-inline-block bg-light myuw-text-sm">
            Library Item Due</span>
          <span class="text-dark d-block fw-bold">
            {{ toFromNowDate(library.next_due) }}
          </span>
        </a>
        <a
          v-else-if="library && library.holds_ready"
          v-inner="'MyUW Accounts page - Library Account'"
          class="d-inline-block col px-3 py-1 ms-1
          fw-light text-dark text-nowrap"
          :class="[
            $mq == 'tablet' || $mq == 'desktop'
              ? 'border-start text-start'
              : 'border-none text-center',
          ]"
          href="/accounts/"
        >
          <span class="d-inline-block bg-light myuw-text-sm">
            Library {{ library.holds_ready === 1 ? 'Items' : 'Item' }} Ready
          </span>
          <span class="text-dark d-block fw-bold">
            {{ library.holds_ready }}
            {{ library.holds_ready === 1 ? 'Items' : 'Item' }} ready
          </span>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import {
  faCalendarAlt,
} from '@fortawesome/free-regular-svg-icons';
import {mapGetters, mapState, mapActions} from 'vuex';

export default {
  data() {
    return {
      faCalendarAlt,
    };
  },
  computed: {
    ...mapState({
      termData: (state) => state.termData,
      alum: (state) => state.user.affiliations.alumni,
      student: (state) => state.user.affiliations.student,
      employee: (state) => state.user.affiliations.all_employee,
      past_stud: (state) => state.user.affiliations.past_stud,
      past_emp: (state) => state.user.affiliations.past_employee,
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
    loadData() {
      return (this.alum || this.student || this.past_stud || this.employee || this.past_emp);
    },
  },
  mounted() {
    if (this.loadData) {
      this.fetchHfs();
      this.fetchLibrary();
    }
  },
  methods: {
    ...mapActions('hfs', {
      fetchHfs: 'fetch',
    }),
    ...mapActions('library', {
      fetchLibrary: 'fetch',
    }),
    getWeeksApart(qsDate, testDate) {
      const days = this.dayjs(testDate).diff(
          this.dayjs(qsDate).startOf('week'),
          'days',
      );
      if (days < 0) {
        return 0;
      } else {
        return parseInt(days / 7) + 1;
      }
    },
    toFromNowDate(s) { return this.dayjs(s).from(this.nowDatetime()); },
  },
};
</script>
