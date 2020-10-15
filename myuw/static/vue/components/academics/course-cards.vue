<template>
  <div v-if="this.student">
    <div v-if="isReady">
      <h3>Your {{ucfirst(course.quarter)}} {{course.year}} Courses</h3>
      <uw-course-card
        v-for="(section, i) in course.sections" :key="i"
        :course="course" :section="section" :index="i"
      />
    </div>
    <uw-card :errored="isErrored" v-else>
      <template #card-heading>
        Schedule &amp; Course Info
      </template>
    </uw-card>
  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../_templates/card.vue';
import CourseCard from '../_common/course/course.vue';

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
  },
  data: function() {
    return {
      term: "current",
    };
  },
  computed: {
    ...mapState({
      student: (state) => state.user.affiliations.student,
    }),
    ...mapState('studSchedule', {
      course(state) {
        return state.value[this.term];
      }
    }),
    ...mapGetters('studSchedule', {
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
    if(this.student) this.fetch(this.term);
  },
  methods: {
    ...mapActions('studSchedule', ['fetch']),
  },
};
</script>