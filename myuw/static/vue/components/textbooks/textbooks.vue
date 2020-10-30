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

      <div>
        <a target="_blank" :href="orderUrl">
          Start textbook shopping
        </a>
      </div>
      <div>
        <div>
          <font-awesome-icon :icon="['fas', 'exclamation-triangle']" />
          <strong>University Book Store autumn 2020 update</strong>
        </div>
        <div>
          In order to ensure public health, all course materials purchases for
          Fall 2020 quarter are online only; University Book Store&rsquo;s
          course materials department will be closed to the public.
        </div>
      </div>

      <div>
        <p>
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
      <font-awesome-icon :icon="['fas', 'exclamation-triangle']" />
      An error has occurred and we can't load this content right now.
      Please try again later.
    </template>
  </uw-panel>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Section from './section.vue';
import Panel from '../_templates/panel.vue';

export default {
  components: {
    'uw-panel': Panel,
    'uw-section': Section,
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
        this.isStudScheduleReady(this.term) &&
        this.isTextbookReady(this.term) &&
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
