<template>
  <uw-card v-if="showContent()" loaded>
    <template #card-heading>
      <h3>
        {{ ucfirst(getQuarter()) }}
        {{ getYear() }} Teaching Schedule
      </h3>
    </template>
    <template #card-body>
      <div v-if="instSchedule.sections.length">
        <div v-if="term !== 'current'">
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
            <a
              :href="`/teaching/${term}`"
              :future-nav-target="`${term}`"
              :data-linklabel="getTeachingLinkLabel()"
              title="Open teaching page"
            >
              View details
            </a>
          </span>
        </div>

        <uw-summer-section-list
          v-if="getQuarter() === 'summer'"
          :schedule="instSchedule"
          :mobile-only="mobileOnly"
        />

        <uw-section-list
          v-else
          :sections="instSchedule.sections"
          :mobile-only="mobileOnly"
        />

        <div>
          <a :href="getAcadCalLink()">
            View
            {{ ucfirst(getQuarter()) }}
            {{ getYear() }}
            important dates and deadlines
          </a>
        </div>
      </div>
      <div v-else>
        <p v-if="term === 'current'">
          You are not teaching any courses this term.
        </p>
      </div>
    </template>
  </uw-card>

  <uw-error
    v-else-if="isErrored"
    :status-code="statusCodeTagged(term)"
    :year="getYear()"
    :quarter="getQuarter()"
    loaded
  />
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';
import Error from './error.vue';
import SectionList from './section-list.vue';
import SummerSectionList from './summer-list.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-error': Error,
    'uw-section-list': SectionList,
    'uw-summer-section-list': SummerSectionList,
  },
  props: {
    term: {
      type: String,
      default: 'current',
    },
    mobileOnly: {
      type: Boolean,
      default: false,
    },
    isFutureTerm: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      isOpen: false,
    };
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
      return (this.instructor && this.isReady() &&
        (this.instSchedule.sections.length || this.term === 'current'));
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
    getYear() {
      return this.term === 'current' ? this.year : this.nextYear;
    },
    getQuarter() {
      return this.term === 'current' ? this.quarter : this.nextQuarter;
    },
    getTeachingLinkLabel() {
      return (this.ucfirst(this.getQuarter()) + ' ' + this.getYear() +
       ' Teaching Details');
    },
    getAcadCalLink() {
      return ('/academic_calendar/#' + this.getYear() + ',' +
        this.getQuarter());
    },
  },
};
</script>
