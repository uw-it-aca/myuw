<template>
  <uw-card v-if="showGradeCard"
           v-meta="{term: term}"
           :loaded="isReady"
           :errored="isErrored"
           :errored-show="showError"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Final Grades
      </h2>
    </template>
    <template #card-body>
      <div v-if="isHomePage">
        <p class="myuw-text-md">
          Final grades are hidden to protect your privacy.<br>
          <a v-uw-collapse="`grades-collapse`"
            v-no-track-collapse
            class="p-0 border-0 mb-2 bg-transparent"
          >View final grades</a>
          <font-awesome-icon v-if="gradesOpen" :icon="faChevronUp" />
          <font-awesome-icon v-else :icon="faChevronDown" />
        </p>
        <uw-collapse
          :id="`grades-collapse`"
          v-model="gradesOpen"
          class="myuw-fin-aid"
        >
          <p
           v-if="!isAfterGradeSubmissionDeadline"
          class="text-muted fst-italic myuw-text-md"
          >
          These grades are not official until 11:59 p.m. on
          {{ toFriendlyDate(gradeSubmissionDeadline) }}.
          </p>
          <uw-grades-panel :sections="filteredSections"/>
        </uw-collapse>
      </div>
      <uw-grades-panel v-else :sections="filteredSections" />
    </template>
    <template #card-disclosure>
      <uw-collapse
        id="grade_card_collapse"
        v-model="gradeResOpen"
      >
        <h3 class="visually-hidden">
          Resources
        </h3>
        <ul class="list-unstyled myuw-text-md">
          <li class="mb-1">
            <a href="https://sdb.admin.uw.edu/sisStudents/uwnetid/grades.aspx">
              View credits and GPA
            </a>
          </li>
          <li class="mb-1">
            <a v-out="'MyPlan DARS'"
               href="https://myplan.uw.edu/audit/#/degree"
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
      </uw-collapse>
    </template>
    <template #card-footer>
      <button v-uw-collapse.grade_card_collapse
        type="button" class="btn btn-link btn-sm w-100 p-0 text-dark"
        title='Additional grade resources'
      >
        Resources
        <font-awesome-icon v-if="gradeResOpen" :icon="faChevronUp" />
        <font-awesome-icon v-else :icon="faChevronDown" />
      </button>
    </template>
  </uw-card>
</template>

<script>
import GradesPanel from './grades-panel.vue';
import {
  faChevronUp,
  faChevronDown,
  faCaretDown,
  faCaretRight,
} from '@fortawesome/free-solid-svg-icons';
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';
import Collapse from '../../_templates/collapse.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-collapse': Collapse,
    'uw-grades-panel': GradesPanel,
  },
  props: {
    isHomePage: {
      type: Boolean,
      default: false,
    },
  },
  data: function() {
    return {
      term: null,
      showOnlyATerm: false,
      gradeResOpen: false,
      gradesOpen: false,
      faChevronUp,
      faChevronDown,
      faCaretDown,
      faCaretRight,
    };
  },
  computed: {
    ...mapState({
      student: (state) => state.user.affiliations.student,
      currentSummerTerm: (state) => state.cardDisplayDates.current_summer_term,
      isAfterLastDayOfClasses: (state) =>
        state.cardDisplayDates.is_after_last_day_of_classes,
      isBeforeFirstDayOfTerm: (state) =>
        state.cardDisplayDates.is_before_first_day_of_term,
      isSummer: (state) => state.cardDisplayDates.is_summer,
      lastTerm: (state) => state.cardDisplayDates.last_term,
      isAfterBtermStart: (state) => state.cardDisplayDates.is_after_summer_b,
      isAfterGradeSubmissionDeadline: (state) =>
        state.cardDisplayDates.is_after_grade_submission_deadline,
      courses: (state) => state.stud_schedule.value,
    }),
    ...mapGetters('stud_schedule', [
      'isReadyTagged',
      'isErroredTagged',
      'statusCodeTagged',
    ]),
    isReady() {
      return this.isReadyTagged(this.term);
    },
    isErrored() {
      return this.isErroredTagged(this.term);
    },
    showError() {
      return this.statusCodeTagged(this.term) !== 404;
    },
    gradeSubmissionDeadline() {
      if (this.term in this.courses) {
        return this.courses[this.term].term.grade_submission_deadline;
      } else {
        return [];
      }
    },
    filteredSections() {
      if (this.term in this.courses) {
        return this.courses[this.term].sections.filter((section) => {
          let shouldDisplay = true; // display grade

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
      } else {
        return [];
      }
    },
    showGradeCard() {
      return (
        this.student &&
        this.term !== null &&
        // This is done so that when there is a error it goes to the second
        // if conditional
        ((!this.isReady && !this.isErrored) ||
          (this.term in this.courses && this.filteredSections.length > 0))
      );
    },
  },
  mounted() {
    if (!this.student) return;
    // display window: [lastDayOfClasses..firstDayOfTerm]
    if (this.isBeforeFirstDayOfTerm) {
      this.term = this.lastTerm;
    } else if (this.isAfterLastDayOfClasses) {
      if (this.isSummer) {
        this.term = this.currentSummerTerm;
      } else {
        this.term = 'current';
      }
    } else if (this.isSummer && this.isAfterBtermStart) {
      this.term = this.currentSummerTerm.concat(',a-term');
      this.showOnlyATerm = true;
    }
    if (this.term) this.fetch(this.term);
  },
  methods: {
    ...mapActions('stud_schedule', ['fetch']),
  },
};
</script>
