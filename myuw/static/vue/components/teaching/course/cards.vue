<template>
  <div v-if="isReady && instSchedule.sections.length">
    <uw-course-card
      v-for="(section, i) in instSchedule.sections"
      :key="i"
      :schedule="instSchedule"
      :section="section"
    />
  </div>
  <uw-card
    v-else
    :loaded="isErrored || (isReady && !instSchedule.sections.length)"
  >
    <template #card-body>
      No courses associated with this term.
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';
import CourseCard from './card.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-course-card': CourseCard,
  },
  props: {
    term: {
      type: String,
      required: true,
    },
  },
  computed: {
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
  watch: {
    // Used to handle cases when the term is changed without remouting
    // the component
    term(newVal, oldVal) {
      this.fetch(this.term);
    },
  },
  mounted() {
    this.fetch(this.term);
  },
  methods: {
    ...mapActions('inst_schedule', {
      fetch: 'fetch',
    }),
  },
};
</script>
