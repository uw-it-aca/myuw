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
  <span v-else>
    <span
      v-uw-collapse="`textbook-${section.anchor}-collapse-${$meta.uid}`"
      v-no-track-collapse
      type="button"
      class="myuw-text-md"
    >
      <span>Textbooks:
        <font-awesome-icon :icon="faExclamationTriangle"/>... How to fix this</span>
    </span>
    <uw-collapse
      :id="`textbook-${section.anchor}-collapse-${$meta.uid}`"
      v-model="collapseOpen"
      tabindex="0"
    >
      <div class="p-3 mt-2 bg-light text-dark notice-body">
        To best accommodates student ...
      </div>
    </uw-collapse>
  </span>
</template>

<script>
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
  computed: {
    term() {
      let term = this.section.year + "," + this.section.quarter;
      if (this.section.summer_term) {
        term = term + ',' + this.section.summer_term.toLowerCase();
      }
      return term
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
