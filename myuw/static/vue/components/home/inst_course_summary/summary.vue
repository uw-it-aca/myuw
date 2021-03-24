<template>
  <uw-card v-if="instructor && showContent"
           v-meta="{term: term}"
           :loaded="isReady"
           :errored="isErrored"
           :errored-show="statusCodeTagged(term) !== 404"
  >
    <template #card-heading>
      <h2 class="h4 text-dark-beige myuw-font-encode-sans">
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
          <!-- diplay only for a future term -->
          <p>
            You are teaching
            <strong>
              {{ instSchedule.sections.length }}
              {{ instSchedule.sections.length > 1 ? 'courses' : 'course' }}
            </strong>.
            <br>
            The first day of instruction is
            {{ toFriendlyDate(instSchedule.term.first_day_quarter) }}
            ({{ toFromNowDate(instSchedule.term.first_day_quarter) }})
          </p>
          <span>
            <b-link
              v-inner="`View details: ${term}`"
              :href="`/teaching/${term}`"
              :future-nav-target="`${term}`"
              :title="getTeachingLinkLabel"
            >
              View details
            </b-link>
          </span>
        </div>

        <uw-summer-section-list v-if="getQuarter === 'summer'" :schedule="instSchedule" />
        <uw-section-list v-else :sections="instSchedule.sections" />

        <div>
          <b-link
            v-inner="`important dates and deadlines: ${term}`"
            :href="getAcadCalLink">
            View {{ titleCaseWord(getQuarter) }} {{ getYear }}
            important dates and deadlines
          </b-link>
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
        target="_blank"
      >
        My Class Instructor Resources
      </a> page.
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';
import SectionList from './section-list.vue';
import SummerSectionList from './summer-list.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-section-list': SectionList,
    'uw-summer-section-list': SummerSectionList,
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
    ...mapGetters('inst_schedule', {
      isReadyTagged: 'isReadyTagged',
      isErroredTagged: 'isErroredTagged',
      statusCodeTagged: 'statusCodeTagged',
    }),
    isReady() {
      return this.isReadyTagged(this.term);
    },
    isErrored() {
      return this.isErroredTagged(this.term);
    },
    showContent() {
      return this.isErrored || this.instSchedule &&
        (this.instSchedule.sections.length || !this.instSchedule.future_term);
    },
    getYear() {
      return this.term === 'current' ? this.year : this.nextYear;
    },
    getQuarter() {
      return this.term === 'current' ? this.quarter : this.nextQuarter;
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
    }
  },
  methods: {
    ...mapActions('inst_schedule', {
      fetchInstSche: 'fetch',
    }),
  },
};
</script>
