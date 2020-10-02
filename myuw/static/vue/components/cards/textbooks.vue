<template>
  <uw-card
    v-if="show"
    :loaded="isReadyTagged(term)"
    :errored="isErroredTagged(term)"
  >
    <template #card-heading>
      <h3>Textbooks</h3>
    </template>
    <template #card-body>
      <ul>
        <li v-for="(section, i) in sections" :key="i">
        </li>
      </ul>
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../containers/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  props: {
    term: {
      type: String,
      required: true,
    }
  },
  computed: {
    ...mapState({
      student: (state) => state.user.affiliations.student,
      isBeforeEndOfFirstWeek: (state) => 
        state.cardDisplayDates.is_before_eof_7days_of_term,
    }),
    ...mapState('textbooks', {
      textbookTerm: (state) => state.value.term,
    }),
    ...mapGetters('textbooks', [
      'isReadyTagged',
      'isErroredTagged',
    ]),
    show() {
      return (
        this.student &&
        (this.term !== 'current' || this.isBeforeEndOfFirstWeek)
      );
    }
  },
  // Called when the function in injected into the page
  created() {
    if (this.show) {
      // We got this fetch function from mapActions
      this.fetchTextbooks(this.term);
      this.fetchSchedule(this.term);
    }
  },
  methods: {
    // Mapping the fetch function from textbooks module
    ...mapActions('textbooks', {
      fetchTextbooks: 'fetch',
    }),
    ...mapActions('schedule', {
      fetchSchedule: 'fetch',
    }),
  },
};
</script>

<style lang="scss" scoped>
</style>
