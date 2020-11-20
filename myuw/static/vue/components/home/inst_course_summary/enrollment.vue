<template>
  <span v-if="section.is_prev_term_enrollment">
    0<!-- the current_enrollment value is of previous term -->
    <span v-if="!section.is_independent_study">
      &nbsp;of&nbsp;{{ section.limit_estimate_enrollment }}
    </span>
  </span>

  <span v-else-if="!section.current_enrollment">
    0<span v-if="!section.is_independent_study">
      &nbsp;of&nbsp;{{ section.limit_estimate_enrollment }}
    </span>
  </span>

  <span v-else>
    <a
      target="_blank"
      :href="classListHref()"
      :rel="section.section_label"
      :title="getTitle()"
    >
      {{ section.current_enrollment }}
      <span v-if="!section.is_independent_study">
        <span>&nbsp;of&nbsp;</span><span aria-hidden="true">/</span>
        {{ section.limit_estimate_enrollment }}
      </span>
    </a>
  </span>
</template>

<script>
export default {
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
  methods: {
    classListHref() {
      return ('/teaching/' + this.section.year + ',' +
              this.section.quarter + ',' + this.section.curriculum_abbr + ',' +
              this.section.course_number + '/' +
              this.section.section_id + '/students');
    },
    getTitle() {
      return ('View class list of ' +
               this.section.curriculum_abbr + ' ' +
               this.section.course_number + ' ' +
               this.section.section_id);
    },
  },
};
</script>
