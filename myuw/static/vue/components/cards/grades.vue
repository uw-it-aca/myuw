<template>
  <uw-card v-if="(!isReady || filteredSections.length > 0) && term"
           :loaded="isReady" :errored="isErrored"
  >
    <template #card-heading>
      <h3>
        Final Grades
      </h3>
    </template>
    <template #card-body>
      <span v-if="!isAfterGradeSubmissionDeadline">
        These grades are not official until 11:59 p.m. on 
        {{toFriendlyDate(gradeSubmissionDeadline)}}.
      </span>
      <ul>
        <li v-for="section in filteredSections" :key="section.course_number">
          <div :class="`bg-c${section.color_id} simplesquare`"
               aria-hidden="true"
          />
          <span>{{section.curriculum_abbr}} {{section.course_number}}</span>
          <span v-if="section.grade === 'X'"> No grade yet</span>
          <span>{{section.grade}}</span>
        </li>
      </ul>
    </template>
    <template #card-disclosure>
      <b-collapse id="grade_card_collapse" v-model="isOpen">
        <h4>Resources</h4>
        <ul>
          <li>
            <a href="https://sdb.admin.uw.edu/sisStudents/uwnetid/grades.aspx">
              View credits and GPA
            </a>
          </li>
          <li>
            <a
              href="https://myplan.uw.edu/audit/login/netid?rd=/student/myplan/dars"
              data-linklabel="MyPlan - Degree Audit"
            >
              Degree Audit Reporting System (DARS)
            </a>
          </li>
          <li>
            <a href="https://sdb.admin.uw.edu/students/uwnetid/unofficial.asp">
              Unofficial Transcript
            </a>
          </li>
        </ul>
      </b-collapse>
    </template>
    <template #card-footer>
      <button v-if="!isOpen"
              v-b-toggle.grade_card_collapse aria-label="SHOW MORE"
      >
        SHOW MORE
      </button>
      <button v-else v-b-toggle.grade_card_collapse aria-label="SHOW LESS">
        SHOW LESS
      </button>
    </template>
  </uw-card>
</template>

<script>
import moment from 'moment';
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../containers/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  data: function () {
    return {
      term: null,
      showOnlyATerm: false,
      isOpen: false,
    }
  },
  computed: {
    ...mapState({
      currentSummerTerm: (state) => state.cardDisplayDates.current_summer_term,
      gradeSubmissionDeadline: (state) =>
        state.courses.value.term.grade_submission_deadline,
      isAfterLastDayOfClasses: (state) =>
        state.cardDisplayDates.is_after_last_day_of_classes,
      isBeforeLastDayOfClasses: (state) =>
        state.cardDisplayDates.is_before_first_day_of_term,
      isSummer: (state) => state.cardDisplayDates.is_summer,
      lastTerm: (state) => state.cardDisplayDates.last_term,
      isAfterSummerBStart: (state) =>
        state.cardDisplayDates.is_after_summer_b,
      isAfterGradeSubmissionDeadline: (state) =>
        state.cardDisplayDates.is_after_grade_submission_deadline,
      sections: (state) => state.courses.value.sections,
    }),
    ...mapGetters('courses', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
    filteredSections: function() {
      return this.sections.filter((section) => {
        let shouldDisplay = true;

        if (this.showOnlyATerm && section.summer_term !== 'A-term') {
          section.hide_for_early_summer_display = true;
          shouldDisplay = false;
        }

        if (section.is_primary_section && !section.is_auditor) {
          if (!section.hide_for_early_summer_display) {
            shouldDisplay = true;
          }
        } else {
          shouldDisplay = false;
        }

        return shouldDisplay;
      });
    }
  },
  mounted() {
    if (this.isAfterLastDayOfClasses) {
      this.term = 'current';

      if (this.isSummer) {
        this.term = this.currentSummerTerm;
      }
    } else if (this.isBeforeLastDayOfClasses) {
      this.term = this.lastTerm;
    } else if (this.isSummer && this.isAfterSummerBStart) {
      this.term = this.currentSummerTerm;
      this.showOnlyATerm = true;
    }
    this.fetch(this.term);
  },
  methods: {
    toFriendlyDate(dateStr) {
      if (dateStr === undefined || dateStr.length === 0) {
            return '';
      }
      return moment(dateStr).format('ddd, MMM D');
    },
    ...mapActions('courses', ['fetch']),
  },
}
</script>

<style lang="scss" scoped>
  .simplesquare {
    display: inline-block;
    height: .9em;
    width: .9em;
    margin-right: 0.3em;
  }
</style>