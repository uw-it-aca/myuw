<template>
  <!-- TODO: Add loading and error handling here -->
  <div v-if="isReady">
    <uw-term-selector
      :current-quarter="quarter"
      :current-year="year"
      :all-tabs="this.instSchedule.related_terms"
    >
      <template #default="slotData">
        <uw-course-cards :term="slotData.tab.label" />
      </template>
    </uw-term-selector>
  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import CourseCards from './cards.vue';
import TermSelector from '../../_common/term-selector.vue';

export default {
  components: {
    'uw-course-cards': CourseCards,
    'uw-term-selector': TermSelector,
  },
  computed: {
    ...mapState({
      year: (state) => parseInt(state.termData.year),
      quarter: (state) => state.termData.quarter,
      term: (state) => `${state.termData.year},${state.termData.quarter}`,
    }),
    ...mapState('inst_schedule', {
      instSchedule(state) {
        return state.value[this.term];
      },
    }),
    ...mapGetters('inst_schedule', {
      isReadyTagged: 'isReadyTagged',
      isErroredTagged: 'isErroredTagged',
    }),
    isReady() {
      return this.isReadyTagged(this.term);
    },
    isErrored() {
      return this.isErroredTagged(this.term);
    },
  },
  created() {
    this.fetch(this.term);
  },
  methods: {
    ...mapActions('inst_schedule', {
      fetch: 'fetch',
    }),
  },
}
</script>