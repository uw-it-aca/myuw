<template>
  <uw-card v-if="showCard"
           v-meta="{term: term}"
           :loaded="isReady"
           :errored="isErrored"
           :errored-show="statusCodeTagged(term) !== 404"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        {{ titleCaseWord(getQuarter) }} {{ getYear }} Teaching Schedule
      </h2>
    </template>
    <template #card-body>
      <div v-if="!instSchedule.sections.length">
        <!-- teach no course -->
        <p>
          You are not teaching any courses this term.
        </p>
      </div>
      <div v-else>
        <!-- teach some courses -->
        <div v-if="instSchedule.future_term">
          <span class="float-end">
            <a
              v-inner="`View details: ${term}`"
              :href="`/teaching/${term}`"
              :future-nav-target="`${term}`"
              :title="getTeachingLinkLabel"
            >
              View details
            </a>
          </span>
          <p class="myuw-text-sm">
            The first day of instruction is
            {{ toFriendlyDate(instSchedule.term.first_day_quarter) }}
            ({{ toFromNowDate(instSchedule.term.first_day_quarter) }})
          </p>
        </div>
        <div v-else-if="hasGradingNotices" class="my-2">
          <uw-collapsed-notice
            :notice="gradingNotice"
            :caller-id="`instSummary${termId}`"
          >
            <template #notice-body>
              <div v-html="gradingNotice.notice_body" />
            </template>
          </uw-collapsed-notice>
          <hr class="bg-secondary">
        </div>

        <uw-summer-section-list v-if="getQuarter === 'summer'" :schedule="instSchedule" />
        <uw-section-list v-else :sections="instSchedule.sections" />

        <uw-collapsed-notice v-if="hasClassResAccNotice"
          :notice="classResAccNotice" :caller-id="`instSummary${termId}`">
          <template #notice-body>
            <div v-html="classResAccNotice.notice_body" />
          </template>
        </uw-collapsed-notice>

        <div class="myuw-text-md">
          <a
            v-inner="`important dates and deadlines: ${term}`"
            :href="getAcadCalLink">
            View {{ titleCaseWord(getQuarter) }} {{ getYear }}
            important dates and deadlines
          </a>
        </div>
      </div>
    </template>

    <template v-if="statusCodeTagged(term) === 410" #card-error>
      The page you seek is for a past quarter and is no longer available.
    </template>
    <template v-else #card-error>
      <i class="fa fa-exclamation-triangle" />
      An error occurred and MyUW cannot load your teaching schedule
      right now. In the meantime, try the
      <a
        href="https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/default.aspx"
      >My Class Instructor Resources</a> page.
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';
import SectionList from './section-list.vue';
import SummerSectionList from './summer-list.vue';
import CollapsedNotice from '../../_common/collapsed-notice.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-section-list': SectionList,
    'uw-summer-section-list': SummerSectionList,
    'uw-collapsed-notice': CollapsedNotice,
  },
  props: {
    term: {
      type: String,
      default: 'current',
    },
  },
  computed: {
    ...mapState({
      instructor: (state) => state.user.affiliations.instructor,
      year: (state) => state.termData.year,
      quarter: (state) => state.termData.quarter,
      nextYear: (state) => state.nextTerm.year,
      nextQuarter: (state) => state.nextTerm.quarter,
    }),
    ...mapState('inst_schedule', {
      instSchedule(state) {
        return state.value[this.term];
      },
    }),
    ...mapState('notices', {
      notices: (state) => state.value,
    }),
    ...mapGetters('inst_schedule', {
      isReadyTagged: 'isReadyTagged',
      isErroredTagged: 'isErroredTagged',
      statusCodeTagged: 'statusCodeTagged',
    }),
    ...mapGetters('notices', {
      isNoticeReady: 'isReady',
      isNoticeErrored: 'isErrored',
    }),
    isReady() {
      return this.isReadyTagged(this.term) && this.isNoticeReady;
    },
    isErrored() {
      return this.isErroredTagged(this.term);
    },
    classResAccNotice() {
      // MUWM-5199
      return this.notices.filter((notice) =>
        notice.category === 'Teaching ClassResAccessible'
      )[0];
    },
    hasClassResAccNotice() {
      return this.instSchedule.future_term && Boolean(this.classResAccNotice);
    },
    gradingNotices() {
      // MUWM-4072
      return this.notices.filter((notice) =>
        notice.category === 'GradeSubmission GradingOpen'
      );
    },
    hasGradingNotices() {
      return this.gradingNotices.length > 0;
    },
    gradingNotice() {
      return {
        notice_body: this.gradingNotices[0].notice_body,
        notice_title: this.gradingNotices[0].notice_title,
        id_hash: this.gradingNotices[0].id_hash,
        is_critical: true,
        is_read: this.gradingNotices[0].is_read
      };
    },
    showCard() {
      return this.instructor && (
        !this.isReady || this.isErrored ||
        this.instSchedule &&
        (this.instSchedule.sections.length || !this.instSchedule.future_term) &&
        (!this.instSchedule.future_term || this.hasClassResAccNotice));
    },
    getYear() {
      return this.term === 'current' ? this.year : this.nextYear;
    },
    getQuarter() {
      return this.term === 'current' ? this.quarter : this.nextQuarter;
    },
    termId() {
      return this.getYear + this.getQuarter;
    },
    getTeachingLinkLabel() {
      return this.titleCaseWord(this.getQuarter) + ' ' + this.getYear +
        ' Teaching details';
    },
    getAcadCalLink() {
      return '/academic_calendar/#' + this.getYear + ',' + this.getQuarter;
    },
  },
  created() {
    if (this.instructor) {
      this.fetchInstSche(this.term);
      this.fetchNotices();
    }
  },
  methods: {
    ...mapActions('inst_schedule', {
      fetchInstSche: 'fetch',
    }),
    ...mapActions('notices', {
      fetchNotices: 'fetch',
    }),
  }
};
</script>
