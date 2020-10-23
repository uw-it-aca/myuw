<template>
  <div v-if="student">
    <div v-if="isReady">
      <h3 class="sr-only">
        Your {{ ucfirst(course.quarter) }} {{ course.year }} Courses
      </h3>
      <uw-course-card
        v-for="(section, i) in course.sections" :key="i"
        :course="course" :section="section" :index="i"
      />
    </div>
    <uw-card v-else-if="isErrored && statusCodeTagged(term) == 404" loaded>
      <template #card-heading>
        No {{ ucfirst(quarter) }} {{ ucfirst(summerTerm) }} Registration Found
      </template>
      <template #card-body>
        <p>
          You don’t appear to be registered for any credit courses in
          {{ quarter }} {{ summerTerm }} quarter. If you think this is an
          error, please
          <a
            :href="helpMyUW"
            title="Send email to help@uw.edu"
          >
            contact MyUW
          </a>.
        </p>

        <p>
          If you are interested in registration,
          <a href="../resource/academics">
            view registration resources.
          </a>
        </p>
      </template>
    </uw-card>
    <uw-card v-else :errored="isErrored">
      <template #card-heading>
        Schedule &amp; Course Info
      </template>
    </uw-card>
  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';
import CourseCard from './course.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-course-card': CourseCard,
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
  data() {
    return {
      // Work around eslint for strings inside vue template
      helpMyUW: 'mailto:help@uw.edu?subject=MyUW%20Comment,%20Request,%20Suggestion&body=Hello,%0A%0A%3CInclude%20your%20comment%20or%20question%20about%20MyUW%20here%3e%0A%0A%0A%0ANetID%3A%20',
    };
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
    if (this.student) this.fetch(this.term);
  },
  methods: {
    ...mapActions('stud_schedule', ['fetch']),
  },
};
</script>
