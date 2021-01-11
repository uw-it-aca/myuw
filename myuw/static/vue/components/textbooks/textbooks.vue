<template>
  <uw-panel :loaded="isReady" :errored="isErrored">
    <template #panel-body>
      <div v-if="bookData.teachingSections.length > 0">
        <h3>Teaching</h3>
        <hr>
        <uw-section
          v-for="(section, i) in bookData.teachingSections"
          :key="i"
          :section="section"
          :collapsable="bookData.collapseSections"
        />
        <hr v-if="bookData.collapseSections">
        <h3 v-if="bookData.enrolledSections">
          Enrolled
        </h3>
        <hr>
      </div>
      <uw-section
        v-for="(section, i) in bookData.enrolledSections"
        :key="i"
        :section="section"
        :collapsable="bookData.collapseSections"
      >
        <template #no-books>
          No textbook requirement has been received for this course.
          Please check with your instructor.
        </template>
      </uw-section>

      <div class="my-4 text-center">
        <uw-link-button target="_blank" :href="orderUrl">
          Start textbook shopping
        </uw-link-button>
      </div>

      <uw-covid />

      <div>
        <p class="text-muted myuw-text-md">
          Information on course textbooks is collected by and provided
          courtesy of
          <a href="http://www.bookstore.washington.edu">
            University Book Store
          </a>
          and is subject to change regularly and without notice.
        </p>
      </div>
    </template>
    <template #panel-error>
      <!-- error message for textbooks -->
      <b-alert show variant="light" class="p-0 border-0 bg-transparent">
        <div class="d-flex text-danger m-0 myuw-text-md">
          <div class="pr-2 flex-shrink-1">
            <font-awesome-icon :icon="['fas', 'exclamation-triangle']" />
          </div>
          <div class="w-100">
            An error has occurred and we can't load this content right now.
            Please try again later.
          </div>
        </div>
      </b-alert>
    </template>
  </uw-panel>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Panel from '../_templates/panel.vue';
import LinkButton from '../_templates/link-button.vue';
import Section from './section.vue';
import Covid from './covid.vue';

export default {
  components: {
    'uw-panel': Panel,
    'uw-section': Section,
    'uw-covid': Covid,
    'uw-link-button': LinkButton,
  },
  props: {
    term: {
      type: String,
      required: true,
    },
  },
  computed: {
    ...mapState('stud_schedule', {
      studSchedule(state) {
        return state.value[this.term];
      },
    }),
    ...mapState('inst_schedule', {
      instSchedule(state) {
        return state.value[this.term];
      },
    }),
    ...mapGetters('stud_schedule', {
      isStudScheduleReady: 'isReadyTagged',
      isStudScheduleErrored: 'isErroredTagged',
      statusCodeStudSchedule: 'statusCodeTagged',
    }),
    ...mapGetters('inst_schedule', {
      isInstScheduleReady: 'isReadyTagged',
      isInstScheduleErrored: 'isErroredTagged',
      statusCodeInstSchedule: 'statusCodeTagged',
    }),
    ...mapGetters('textbooks', {
      isTextbookReady: 'isReadyTagged',
      isTextbookErrored: 'isErroredTagged',
      statusCodeTextbooks: 'statusCodeTagged',
      getProcessedData: 'getProcessedData',
    }),
    isReady() {
      return (
        this.isTextbookReady(this.term) &&
        (
          this.isStudScheduleReady(this.term) ||
          this.isStudScheduleErrored(this.term)
        ) &&
        (
          this.isInstScheduleReady(this.term) ||
          this.isInstScheduleErrored(this.term)
        )
      );
    },
    isErrored() {
      return (
        this.isStudScheduleErrored(this.term) ||
        this.isTextbookErrored(this.term)
      );
    },
    bookData() {
      if (this.isReady) {
        return this.getProcessedData(this.studSchedule, this.instSchedule);
      }
      return {};
    },
    orderUrl() {
      if (this.bookData.order_url) {
        return this.bookData.order_url;
      }
      return 'http://www.ubookstore.com/adoption-search';
    },
  },
  created() {
    this.fetchStudSchedule(this.term);
    this.fetchInstSchedule(this.term);
    this.fetchTextbooks(this.term);
  },
  methods: {
    ...mapActions('stud_schedule', {
      fetchStudSchedule: 'fetch',
    }),
    ...mapActions('inst_schedule', {
      fetchInstSchedule: 'fetch',
    }),
    ...mapActions('textbooks', {
      fetchTextbooks: 'fetch',
    }),
  },
};
</script>
