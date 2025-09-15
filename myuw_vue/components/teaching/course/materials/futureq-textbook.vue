<template>
  <span v-if="uwtCourse">
    <uw-textbook :section="section" />
    <div class="myuw-text-sm fst-italic">
      If you have not submitted course materials, please
      <a href="mailto:UWTCourseMaterials@uw.edu">email them toUWTCourseMaterials@uw.edu</a>.
    </div>
  </span>
  <span v-else-if="hasBooks">
    <uw-textbook :section="section" />
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
    <uw-collapsed-item
      :part="fixTextbook"
      button-style="mb-2 bg-transparent"
      caller-id="futureTextbook"
    >
      <template #collapsed-body>
        Use the
        <a href="https://ubookstore.com/pages/faculty">
          UW Bookstore Course Materials Request Form </a>
          to provide a list of required reading materials for your course as early as possible.<br>
        
          <br>To best accommodate students, list ALL the required reading materials for your 
          courses, regardless of whether you want UW Bookstore to supply the materials, or to 
          clarify if no texts are required for your course.
      </template>
    </uw-collapsed-item>
  </span>
</template>

<script>
// MUWM-5229
import {mapGetters, mapState, mapActions} from 'vuex';
import {
    faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';
import CollapsedItem from '../../../_common/collapsed-part.vue';
import TextbookLink from '../../../_common/course/textbook.vue';
export default {
  components: {
    'uw-collapsed-item': CollapsedItem,
    'uw-textbook': TextbookLink,
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
        return (book && book.course_id);   // MUWM-5420
      }
      return false;
    },
    dataError() {
      const statusCode = this.statusCode(this.term);
      return statusCode !== 200;
    },
    uwtCourse() {
      return this.section.course_campus.toLowerCase() === 'tacoma';
    },
    fixTextbook() {
      return {
        title: 'How to fix this',
        id: 'fixTextbook' + this.section.sln,
      };
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
