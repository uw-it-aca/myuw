<template>
  <span v-if="hasBooks"> <!-- and does not have books -->
    <a
      v-if="section.sln"
      :href="textbookUrl"
      :title="`Textbooks of ${section.label}`"
    >
      Textbooks
    </a>
  </span>
  <span v-else-if="noDataError">
    <span>
      <font-awesome-icon :icon="faExclamationTriangle" class="text-secondary" /> Missing: Course textbook information in Time Schedule.
    </span>
    <span
      v-uw-collapse="`textbook-${section.anchor}-collapse-${$meta.uid}`"
      v-no-track-collapse
      type="button"
      class="myuw-text-md"
    >
      <span>
        How to fix this
      </span>
    </span>
    <uw-collapse
      :id="`textbook-${section.anchor}-collapse-${$meta.uid}`"
      v-model="collapseOpen"
      tabindex="0"
    >
      <div class="p-3 mt-2 bg-light text-dark notice-body">
        To best accommodate students, it is important to provide a list of required reading
        materials for your course as early as possible. To do this, you should use the
        <a href="http://www2.bookstore.washington.edu/textsys/TextReqLogin.taf?school=uwmain">
          UW Bookstore Course Materials Request Form </a>
        to list ALL the required reading materials for your courses, regardless of whether
        you want UW Bookstore to supply the materials, or to clarify if no texts are required
        for your course.<br>

        <br>Please see the <a href="https://www.ubookstore.com/faculty">UW Bookstore’s
        Faculty Adoptions FAQ</a> for information about how to submit your requests to help
        clarify for students what your required reading materials are.
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
    };
  },
  data () {
    return {
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
    noDataError() {
      const statusCode = this.statusCode(this.term);
      return statusCode === 200;
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
