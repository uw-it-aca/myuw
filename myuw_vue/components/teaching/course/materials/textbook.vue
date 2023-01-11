<template>
  <span v-if="noDBookData || noBook">
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
  },
  computed: {
    term() {
      return this.section.year + "," + this.section.quarter;
    },
    loadData() {
      return this.section.futureTerm;
    },
    ...mapState('textbooks', {
      bookData(state) {
        return state.value[this.term];
      },
    }),
    ...mapGetters('textbooks', {
      isTextbookReady: 'isReadyTagged',
      isTextbookErrored: 'isrroredTagged',
      statusCodeTextbooks: 'statusCodeTagged',
    }),
    isReady() {
      return this.loadData && this.isTextbookReady(this.term);
    },
    noDBookData() {
      return this.loadData && this.statusCodeTextbooks(this.term) === 404;
    },
    noBook() {
      if (!this.loadData) return false;
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
    if (this.loadData) this.fetchTextbooks(this.term);
  },
  methods: {
    ...mapActions('textbooks', {
      fetchTextbooks: 'fetch',
    }),
  },
};
</script>
