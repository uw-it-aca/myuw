<template>
  <span v-if="noDBookData || isReady && noBook">
    New alert
  </span>
  <span v-else>
    <a
      v-if="section.sln"
      :href="textbookUrl"
      :title="`Textbooks of ${section.label}`"
    >
      Textbooks
    </a>
  </span>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
export default {
  props: {
    section: {
      type: Object,
      required: true,
    },
    tabTerm: {
      type: String,
      required: true,
    },
  },
  computed: {
    ...mapState('textbooks', {
      bookData(state) {
        return state.value;
      },
    }),
    ...mapGetters('textbooks', {
      isTextbookReady: 'isReadyTagged',
      isTextbookErrored: 'isrroredTagged',
      statusCodeTextbooks: 'statusCodeTagged',
    }),
    isReady() {
      return this.isTextbookReady(this.tabTerm);
    },
    noDBookData() {
      return this.statusCodeTextbooks(this.tabTerm) === 404;
    },
    noBook() {
      if (this.isReady && this.bookData) {
        const book = this.bookData[this.section.sln];
        return !(book && book.length > 0);
      }
      return true;
    },
    textbookUrl() {
      let url = "/textbooks/" + this.section.year + ',' + this.section.quarter;
      if (this.section.summer_term) {
        url = url + ',' + this.section.summer_term.toLowerCase();
      }
      return url + '#' + this.section.curriculum_abbr +
        this.section.course_number + this.section.section_id;
    }
  },
  mounted() {
    this.fetchTextbooks(this.tabTerm);
  },
  watch: {
    // Used to handle cases when the term is changed without remouting
    // the component
    tabTerm(newVal, oldVal) {
      this.fetchTextbooks(this.tabTerm);
    },
  },
  methods: {
    ...mapActions('textbooks', {
      fetchTextbooks: 'fetch',
    }),
  },
};
</script>
