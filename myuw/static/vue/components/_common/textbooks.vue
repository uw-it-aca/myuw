<template>
  <uw-card
    v-if="show"
    :loaded="isReadyTextbook(term) && isReadySchedule(term)"
    :errored="isErroredTextbook(term) || isErroredSchedule(term)"
    :errored-show="showError"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Textbooks
      </h2>
    </template>
    <template #card-body>
      <ul class="list-unstyled mb-0 myuw-text-md">
        <li v-for="(section, i) in bookData.sections" :key="i" class="d-flex">
          <div class="w-50">
            <font-awesome-icon
              :icon="faSquareFull"
              :class="`text-c${section.colorId}`"
              class="mr-1"
            />
            <span>
              {{ section.courseId }}:
            </span>
          </div>
          <div class="w-50">
            <span v-if="section.noCourseBooks" class="font-weight-bold">
              No books
            </span>
            <span v-else class="font-weight-bold">
              {{ section.totalBooks }}
              {{ section.totalBooks > 1 ? 'books' : 'book' }}
              <span class="font-weight-normal font-italic">
                ({{ section.requiredBooks ? section.requiredBooks : 'not' }}
                required)
              </span>
            </span>
          </div>
        </li>
      </ul>
      <div v-if="!bookData.noBookAssigned"
           class="myuw-chevron"
      >
        <a
          v-inner="`Textbooks: ${bookData.year} ${bookData.quarter}`"
          :href="`/textbooks/${bookData.year},${bookData.quarter}${
          bookData.summerTerm ? ',' + bookData.summerTerm : ''}`"
          :title="`View Textbooks of ${bookData.year} ${bookData.quarter}`"
        >
          <font-awesome-icon :icon="faChevronRight" />
        </a>
      </div>
    </template>
  </uw-card>
</template>

<script>
import {
  faSquareFull,
  faChevronRight,
} from '@fortawesome/free-solid-svg-icons';
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  props: {
    term: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      faSquareFull,
      faChevronRight,
    };
  },
  computed: {
    ...mapState({
      student: (state) => state.user.affiliations.student,
      isBeforeEndOfFirstWeek: (state) =>
        state.cardDisplayDates.is_before_eof_7days_of_term,
    }),
    ...mapState('stud_schedule', {
      courseData: function(state) {
        return state.value[this.term];
      },
    }),
    ...mapGetters('stud_schedule', {
      isReadySchedule: 'isReadyTagged',
      isErroredSchedule: 'isErroredTagged',
      statusCodeSchedule: 'statusCodeTagged',
    }),
    ...mapGetters('textbooks', {
      isReadyTextbook: 'isReadyTagged',
      isErroredTextbook: 'isErroredTagged',
      statusCodeTextbooks: 'statusCodeTagged',
      getProcessedData: 'getProcessedData',
    }),
    show() {
      return (
        this.student &&
        (this.term !== 'current' || this.isBeforeEndOfFirstWeek)
      );
    },
    showError() {
      return (
        this.statusCodeSchedule(this.term) != 404 &&
        this.statusCodeTextbooks(this.term) != 404
      );
    },
    bookData() {
      if (this.isReadyTextbook(this.term) && this.isReadySchedule(this.term)) {
        const data = this.getProcessedData(this.courseData);
        let noBookAssigned = true;
        const sectionBookData = [];

        data.enrolledSections.forEach((section) => {
          let required = 0;
          let optional = 0;
          if (section.books) {
            section.books.forEach((book) => {
              if (book.is_required) {
                required += 1;
              } else {
                optional += 1;
              }
              if (noBookAssigned) {
                noBookAssigned = false;
              }
            });
          }
          const courseId = `${section.curriculum} ${section.courseNumber} ${
            section.sectionId
          }`;

          const sectionData = {
            courseId: courseId,
            colorId: section.colorId,
            requiredBooks: required,
            totalBooks: required + optional,
            noCourseBooks: (required + optional) ? false :true,
          };
          sectionBookData.push(sectionData);
        });

        return {
          noBookAssigned: noBookAssigned,
          quarter: data.quarter,
          year: data.year,
          summerTerm: data.summerTerm,
          sections: sectionBookData,
        };
      }
      return {};
    },
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
    ...mapActions('stud_schedule', {
      fetchSchedule: 'fetch',
    }),
  },
};
</script>

<style lang="scss" scoped>
</style>
