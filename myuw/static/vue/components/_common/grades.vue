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
      <p
        v-if="!isAfterGradeSubmissionDeadline"
        class="text-muted font-italic myuw-text-md"
      >
        These grades are not official until 11:59 p.m. on
        {{ toFriendlyDate(gradeSubmissionDeadline) }}.
      </p>
      <ul class="list-unstyled">
        <li
          v-for="section in filteredSections"
          :key="section.course_number"
          class="mb-2"
        >
          <div class="d-flex align-content-center">
            <div class="w-50">
              <font-awesome-icon
                :icon="faSquareFull"
                :class="`text-c${section.color_id}`"
                class="mr-1"
              />
              <span class="h6 myuw-font-encode-sans m-0">
                {{ section.curriculum_abbr }} {{ section.course_number }}
              </span>
            </div>
            <div class="w-50 text-right text-nowrap">
              <span
                v-if="section.grade === 'X'"
                class="m-0 mr-2 text-muted font-italic myuw-text-md"
              >
                No grade yet
              </span>
              <span class="h6 myuw-font-encode-sans m-0">
                {{ section.grade }}
              </span>
            </div>
          </div>
        </li>
      </ul>
    </template>
    <template #card-disclosure>
      <uw-collapse :collapse-id="`grade_card_collapse`">
        <template #collapsible>
          <h3 class="sr-only">
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
                href="https://myplan.uw.edu/dars"
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
        </template>
      </uw-collapse>
    </template>
    <template #card-footer>
      <button
        data-toggle="collapse"
        data-target="#grade_card_collapse"
        aria-controls="grade_card_collapse"
        aria-expanded="false"
        aria-label="Toggle grade resources"
        type="button"
        class="btn btn-link btn-sm w-100 p-0 text-dark"
        title='Toggle grade resources'
      >
        Resources
        <font-awesome-icon v-if="isOpen" :icon="faChevronUp" />
        <font-awesome-icon v-else :icon="faChevronDown" />
      </button>
    </template>
  </uw-card>
</template>

<script>
import {
  faChevronUp,
  faChevronDown,
  faSquareFull,
} from '@fortawesome/free-solid-svg-icons';
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../_templates/card.vue';
import Collapsible from '../_templates/collapsible.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-collapse': Collapsible,
  },
  data: function() {
    return {
      term: null,
      showOnlyATerm: false,
      isOpen: false,
      faChevronUp,
      faChevronDown,
      faSquareFull,
    };
  },
  computed: {
    ...mapState({
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
    gradeSubmissionDeadline: function() {
      if (this.term in this.courses) {
        return this.courses[this.term].term.grade_submission_deadline;
      } else {
        return [];
      }
    },
    filteredSections: function() {
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
    showGradeCard: function() {
      return (
        this.term &&
        // This is done so that when there is a error it goes to the second
        // if conditional
        ((!this.isReady && !this.isErrored) ||
          (this.term in this.courses && this.filteredSections.length > 0))
      );
    },
  },
  mounted() {
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
