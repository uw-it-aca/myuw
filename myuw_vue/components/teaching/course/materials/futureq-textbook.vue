<template>
  <span v-if="hasBooks">
    <a
      v-if="section.sln"
      :href="textbookUrl"
      :title="`Textbooks of ${section.label}`"
    >
      Textbooks
    </a>
  </span>
  <span v-else-if="dataError">
    Textbooks: <font-awesome-icon :icon="faExclamationTriangle" class="text-danger" />
     <span class="text-danger">An error occurred and MyUW cannot load textbook 
      information right now. Please try again later.</span>
  </span>
  <span v-else>
    Textbook: 
    <span>
      <font-awesome-icon :icon="faExclamationTriangle" class="text-secondary" />
      Clarify course materials requirements in Time Schedule.
    </span>
    <a
      v-uw-collapse="`textbook-${section.anchor}-collapse-${$meta.uid}`"
      v-no-track-collapse
      class="p-0 border-0 mb-2 bg-transparent"
    >How to fix this</a>
    <uw-collapse
      :id="`textbook-${section.anchor}-collapse-${$meta.uid}`"
      v-model="collapseOpen"
      class="myuw-fin-aid"
    >
      <div class="p-3 mt-2 bg-light text-dark notice-body">
        Use the
        <a href="https://www.ubookstore.com/faculty">
          UW Bookstore Course Materials Request Form </a>
          to provide a list of required reading materials for your course as early as possible.<br>
        
          <br>To best accommodate students, list ALL the required reading materials for your 
          courses, regardless of whether you want UW Bookstore to supply the materials, or to 
          clarify if no texts are required for your course.
      </div>
    </uw-collapse>
  </span>
</template>

<script>
// MUWM-5229
import {mapGetters, mapState, mapActions} from 'vuex';
import {
    faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';
import Collapse from '../../../_templates/collapse.vue';
export default {
  components: {
    'uw-collapse': Collapse,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
  data: function() {
    return {
      collapseOpen: false,
      faExclamationTriangle,
    }
  },
  computed: {
    term() {
      return this.section.year + "," + this.section.quarter;
    },
    ...mapState('textbooks', {
      bookData(state) {
        return state.value;
      },
    }),
    ...mapGetters('textbooks', {
      isDataReady: 'isReadyTagged',
      isErrored: 'isErroredTagged',
      statusCode: 'statusCodeTagged',
    }),
    hasBooks() {
      const ready = this.isDataReady(this.term);
      if (ready && this.bookData) {
        const book = this.bookData[this.section.sln];
        return (book && book.length > 0);
      }
      return false;
    },
    dataError() {
      const statusCode = this.statusCode(this.term);
      return statusCode !== 200;
    },
    textbookUrl() {
      return ("/textbooks/" + this.term + '#' + 
        this.section.curriculum_abbr +
        this.section.course_number + this.section.section_id);
    }
  },
  created() {
    this.fetch(this.term);
  },
  methods: {
    ...mapActions('textbooks', {
      fetch: 'fetch',
    }),
  },
};
</script>
<style lang="scss" scoped>
@use "sass:map";
@import '../../../../../myuw/static/css/myuw/variables.scss';
</style>