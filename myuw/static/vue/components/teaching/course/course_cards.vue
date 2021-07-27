<template>
  <div
    v-if="isReady && instSchedule.sections.length"
    v-meta="{tag: `teaching-course-cards`, groupRoot: true}"
  >
    <div v-for="(section, i) in instSchedule.sections" :key="i">
      <uw-course-card
        v-if="section.is_primary_section || !section.isLinkedSecondary"
        :schedule="instSchedule"
        :section="section"
      />
      <div v-else
        :id="`collapse-${section.section_label}`"
        class="collapse"
        :visible="section.mini_card"
      >
        <uw-mini-course-card
          :schedule="instSchedule"
          :section="section"
        />
      </div>
    </div>
  </div>
  <uw-card
    v-else
    :loaded="(isErrored && is404) || (isReady && !instSchedule.sections.length)"
    :errored="isErrored && !is404"
  >
    <template #card-body>
      No courses associated with this term.
    </template>
    <template #card-error>
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
import CourseCard from './course_content.vue';
import MiniCourseCard from './mini-card.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-course-card': CourseCard,
    'uw-mini-course-card': MiniCourseCard,
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
      statusCodeTagged: 'statusCodeTagged',
    }),
    isReady() {
      return this.isReadyTagged(this.term);
    },
    isErrored() {
      return this.isErroredTagged(this.term);
    },
    is404() {
      return this.statusCodeTagged(this.term) === 404;
    }
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
