<template>
  <div v-if="student"
       v-meta="{tag: `student-course-cards`, groupRoot: true}"
  >
    <template v-if="isReady">
      <uw-course-card
        v-for="(section, i) in course.sections" :key="i"
        :term=term :course="course" :section="section" :index="i"
      />
    </template>
    <uw-no-course-card
      v-else-if="isErrored && statusCodeTagged(term) == 404" loaded
      :quarter="quarter" :summer-term="summerTerm"
    />
    <uw-card v-else :errored="isErrored">
      <template #card-heading>
        <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
          Your Courses of {{ titleCaseName(term.replace(',', ' ')) }} Quarter
        </h2>
      </template>
    </uw-card>
  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../../_templates/card.vue';
import CourseCard from './course.vue';
import NoCourseCard from '../no-course.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-course-card': CourseCard,
    'uw-no-course-card': NoCourseCard,
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
      student: (state) => state.user.affiliations.student,
      quarter: (state) => state.termData.quarter,
      summerTerm: (state) => state.termData.summer_term,
    }),
    ...mapState('stud_schedule', {
      course(state) {
        return state.value[this.term];
      },
    }),
    ...mapGetters('stud_schedule', {
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
  },
  created() {
    if (this.student) {
      this.fetchStudSche(this.term);
      this.fetchEvalData();
    }
  },

  methods: {
    ...mapActions('stud_schedule', {
      fetchStudSche: 'fetch',
    }),
    ...mapActions('iasystem', {
      fetchEvalData: 'fetch',
    }),
  },
};
</script>
