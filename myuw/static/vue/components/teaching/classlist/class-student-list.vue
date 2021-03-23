<template>
  <uw-card v-if="showCard"
           :loaded="isReady"
           :errored="isErrored"
  >
    <template #card-heading>
      <div v-if="sectionData">
        <h2>
          {{ sectionData.currAbbr }} {{ sectionData.courseNum }}
          {{ sectionData.sectionId }},
          {{ sectionData.quarter }} {{ sectionData.year }}
        </h2>
        <div v-if="sectionData.sln">
          <h3>SLN</h3>
          <span>{{ sectionData.sln }}</span>
        </div>
      </div>
    </template>

    <template #card-body>
      <div>
        <uw-course-stats
          v-if="sectionData.current"
          :curr-abbr="sectionData.currAbbr"
          :course-num="sectionData.courseNum"
          :section-id="sectionData.sectionId"
          :quarter="sectionData.quarter"
          :year="sectionData.year"
          :majors="sectionData.sections[0].current_student_majors"
        />

        <uw-classlist-content :section="sectionData.sections[0]" />
      </div>
    </template>

    <template v-if="noData" #card-error>
      No class information was found.
    </template>
    <template v-else-if="noAccessPermission" #card-error>
      You need to be the class instructor to view student information.
    </template>
    <template v-else-if="invalidCourse" #card-error>
      The page you seek is for a past quarter and is no longer available.
    </template>
    <template v-else-if="dataError" #card-error>
      An error occurred and MyUW cannot load the class student information
      right now. Please try again later.
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';
import CourseStats from './statistics.vue';
import Content from './content.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-course-stats': CourseStats,
    'uw-classlist-content': Content,
  },
  props: {
    sectionLabel: {
      type: String,
      required: true,
    },
    mobileOnly: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapState({
      instructor: (state) => state.user.affiliations.instructor,
    }),
    ...mapState('classlist', {
      allData: (state) => state.value,
    }),
    ...mapGetters('classlist', {
      isReadyTagged: 'isReadyTagged',
      isErroredTagged: 'isErroredTagged',
      statusCodeTagged: 'statusCodeTagged',
    }),
    getKey() {
      return this.sectionLabel.replace(/&amp;/g, '%26');
    },
    isReady() {
      return this.isReadyTagged(this.getKey);
    },
    sectionData() {
      return this.allData[this.getKey];
    },
    isErrored() {
      return this.isErroredTagged(this.getKey);
    },
    showContent() {
      return this.sectionData && this.sectionData.sections.length &&
        this.sectionData.sections[0].registrations.length;
    },
    showCard() {
      return this.instructor &&
        (!this.isReady || this.isErrored || this.showContent);
    },
    getErrorCode() {
      return this.statusCodeTagged(this.getKey);
    },
    noAccessPermission() {
      return this.getErrorCode === 403;
    },
    noData() {
      return this.getErrorCode === 404;
    },
    invalidCourse() {
      return this.getErrorCode === 410;
    },
    dataError() {
      return this.isErrored && !(this.noData ||
        this.noAccessPermission || this.invalidCourse);
    },
  },
  created() {
    if (this.instructor) {
      this.fetchClasslist(this.getKey);
    }
  },
  methods: {
    ...mapActions('classlist', {
      fetchClasslist: 'fetch',
    }),
  },
};
</script>
