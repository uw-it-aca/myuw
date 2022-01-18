<template>
  <uw-panel :loaded="isReady" :errored="isErrored">
    <template #panel-body>
      <div v-if="bookData.teachingSections.length > 0">
        <h2 class="h5">Teaching</h2>
        <hr class="bg-secondary">
        <uw-section
          v-for="(section, i) in bookData.teachingSections"
          :key="i"
          :section="section"
          :collapsable="bookData.collapseSections"
        />
        <hr v-if="bookData.collapseSections" class="bg-secondary">
        <div v-if="bookData.enrolledSections.length > 0">
          <h2 class="h5">
            Enrolled
          </h2>
          <hr class="bg-secondary">
        </div>
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
        <uw-link-button :href="orderUrl">
          Start textbook shopping
        </uw-link-button>
      </div>

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
      <div class="alert alert-light p-0 border-0 bg-transparent" role="alert">
        <div class="d-flex text-danger m-0 myuw-text-md">
          <div class="pe-2 flex-shrink-1">
            <font-awesome-icon :icon="faExclamationTriangle" />
          </div>
          <div class="w-100">
            An error has occurred and we can't load this content right now.
            Please try again later.
          </div>
        </div>
      </div>
    </template>
  </uw-panel>
</template>

<script>
import {
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';
import {mapGetters, mapState, mapActions} from 'vuex';
import Panel from '../_templates/panel.vue';
import LinkButton from '../_templates/link-button.vue';
import Section from './section.vue';

export default {
  components: {
    'uw-panel': Panel,
    'uw-section': Section,
    'uw-link-button': LinkButton,
  },
  props: {
    term: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      faExclamationTriangle,
    };
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
      return this.isTextbookErrored(this.term);
    },
    bookData() {
      if (this.isReady) {
        return this.getProcessedData(this.studSchedule, this.instSchedule);
      }
      return {};
    },
    orderUrl() {
      if (this.bookData.orderUrl) {
        return this.bookData.orderUrl;
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
