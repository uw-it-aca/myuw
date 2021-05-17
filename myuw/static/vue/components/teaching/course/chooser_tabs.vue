<template>
  <!-- TODO: Add loading and error handling here -->
  <div v-if="instructor">
    <uw-term-selector
      v-if="isReady"
      v-model="term"
      :current-quarter="quarter"
      :current-year="year"
      :all-tabs="instSchedule.related_terms"
    >
      <template #default="slotData">
        <uw-teaching-course-cards :term="slotData.tab.label" />
      </template>
    </uw-term-selector>
    <uw-card v-else :errored="isErrored">
      <template #card-error v-if="statusCodeTagged(fetchTerm) === 404">
        No courses associated with this term.
      </template>
      <template #card-error v-else>
        <i class="fa fa-exclamation-triangle" />
        An error occurred and MyUW cannot load your teaching schedule
        right now. In the meantime, try the
        <a
          href="https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/default.aspx"
        >My Class Instructor Resources</a> page.
      </template>
    </uw-card>
  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';
import CourseCards from './course_cards.vue';
import TermSelector from '../../_common/term-selector.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-teaching-course-cards': CourseCards,
    'uw-term-selector': TermSelector,
  },
  data() {
    return {
      term: window.location.pathname.replace("/teaching/", ""),
      // Fetch term is required because instSchedule.related_terms
      // is depended on the the first fetch and we need to keep track
      // of that term to render the tabs while the actual term is 
      // loading.
      fetchTerm: null,
    }
  },
  computed: {
    ...mapState({
      year: (state) => parseInt(state.termData.year),
      quarter: (state) => state.termData.quarter,
      instructor: (state) => state.user.affiliations.instructor,
    }),
    ...mapState('inst_schedule', {
      instSchedule(state) {
        return state.value[this.fetchTerm];
      },
    }),
    ...mapGetters('inst_schedule', {
      isReadyTagged: 'isReadyTagged',
      isErroredTagged: 'isErroredTagged',
      statusCodeTagged: 'statusCodeTagged',
    }),
    isReady() {
      return this.isReadyTagged(this.fetchTerm);
    },
    isErrored() {
      return this.isErroredTagged(this.fetchTerm);
    },
    showError() {
      return this.statusCodeTagged(this.fetchTerm) !== 404;
    },
  },
  watch: {
    term(value) {
      window.history.replaceState({}, null, `/teaching/${value}`);
    }
  },
  created() {
    if (this.term === "") {
      this.term = `${this.year},${this.quarter}`;
    }
    this.fetchTerm = this.term;
    this.fetch(this.fetchTerm);
  },
  methods: {
    ...mapActions('inst_schedule', {
      fetch: 'fetch',
    }),
  },
};
</script>
