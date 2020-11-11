<template>
  <div v-if="instructor">
    <uw-card v-if="isReady" loaded>
      <template #card-heading>
        <h3>{{ cardHeading }}</h3>
      </template>
      <template #card-body>
        <p v-if="!instSchedule.sections.length">
          You are not teaching any courses.
        </p>
        <div v-else>
        <uw-section-summarys
          v-for="(section, i) in instSchedule.sections"
          :key="i"
          :schedule="instSchedule"
          :section="section" :index="i"
        />
        <div>
          <a :href="`/academic_calendar/#${year},${quarter}`">
            View {{ ucfirst(quarter) }} {{ year }} important dates
            and deadlines
          </a>
        </div>
        </div>
      </template>
    </uw-card>

    <uw-card v-else-if="isErrored && statusCodeTagged(term) == 404" loaded>
      <template #card-heading>
        <h3>{{ cardHeading }}</h3>
      </template>
      <template #card-body>
        <p>
          <i class="fa fa-exclamation-triangle"/>
          An error occurred and MyUW cannot load your teaching schedule
          right now. In the meantime, try the 
          <a
            href="https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/default.aspx"
            data-linklabel="MyClass" target="_blank">
              My Class Instructor Resources
          </a> page.
        </p>
      </template>
    </uw-card>

  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';
import SectionSummary from './section-summary.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-section-summary': SectionSummary,
  },
  props: {
    mobileOnly: {
      type: Boolean,
      default: false,
    },
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
      summerTerm: (state) => state.termData.summer_term,
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
    cardHeading() {
      return ucfirst(quarter).concat(year).concat("Teaching Schedule");
    },
  },

  mounted() {
    this.fetch(this.term);
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
