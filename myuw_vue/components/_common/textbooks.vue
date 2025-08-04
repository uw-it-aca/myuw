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
      <ul class="list-unstyled mb-2 myuw-text-md">
        <li v-for="(section, i) in bookData.sections" :key="i"
          class="d-flex mb-2">
          <div class="w-50">
            <font-awesome-icon
              :icon="faSquareFull"
              :class="`text-c${section.colorId}`"
              class="me-1"
            />
            <span>
              {{ section.courseId }}:
            </span>
          </div>
          <div class="w-50">
            <template v-if="section.viewUWTBookUrl">
              <a :href="section.viewUWTBookUrl">
                Check textbooks
              </a>
            </template>
            <template v-else-if="section.showBData">
              <span v-if="section.hasBookError" class="text-danger"
                title="An error has occurred when loading the textbook requirement for this course"
              >
                Error loading textbooks
              </span>
              <span v-else-if="section.noBookSpecified" title="Please check with your instructor.">
                No textbook specified
              </span>
              <template v-else>
                <span class="myuw-font-encode-sans">
                  {{ section.totalBooks }}
                  {{ section.totalBooks > 1 ? 'books' : 'book' }}
                </span>
                <span class="fw-normal fst-italic">
                    ({{ section.requiredBooks ? section.requiredBooks : 'not' }}
                    required)
                </span>
              </template>
            </template>
          </div>
        </li>
      </ul>
      <div v-if="bookData.hasBookAssigned"
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
        this.isErroredSchedule(this.term) &&
        this.statusCodeSchedule(this.term) != 404 ||
        this.isErroredTextbook(this.term) &&
        this.statusCodeTextbooks(this.term) != 404
      );
    },
    bookData() {
      if (this.isReadyTextbook(this.term) && this.isReadySchedule(this.term)) {
        const data = this.getProcessedData(this.courseData);
        let hasBookAssigned = false;
        const sectionBookData = [];

        data.enrolledSections.forEach((section) => {
          const sectionData = {
            colorId: section.colorId,
            courseId: `${section.curriculum} ${section.courseNumber} ${section.sectionId}`,
            viewUWTBookUrl: section.tacomaCampus ? `/textbooks/uwt/${section.sln}` : null
          };
          // MUWM-5420
          if (section.bookData !== undefined) {
            sectionData.showBData = true;
            sectionData.hasBookError = section.bookData.error !== undefined;

            if (section.bookData.books) {
              sectionData.noBookSpecified = section.bookData.books.length === 0;
              if (!sectionData.noBookSpecified) {
                let required = 0;
                let optional = 0;
                section.bookData.books.forEach((book) => {
                  if (book.is_required) {
                    required += 1;
                  } else {
                    optional += 1;
                  }
                });
                sectionData.requiredBooks = required;
                sectionData.totalBooks = required + optional;
              }
            }

            if (!hasBookAssigned) {
              hasBookAssigned = sectionData.totalBooks > 0;
            }
          }
          sectionBookData.push(sectionData);
        });

        return {
          hasBookAssigned: hasBookAssigned,
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
