<template>
  <span v-if="section.isPrevTermEnrollment">
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
    <b-link
      v-out="`View Classlist: ${section.id}`"
      target="_blank"
      :href="classListHref()"
      :title="getTitle()"
    >
      {{ section.current_enrollment }}
      <span v-if="!section.is_independent_study">
        <span>&nbsp;of&nbsp;</span>
        {{ section.limit_estimate_enrollment }}
      </span>
    </b-link>
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
      return ('/teaching/' + this.section.apiTag + '/students');
    },
    getTitle() {
      return ('View Classlist of ' +
               this.section.curriculum_abbr + ' ' +
               this.section.course_number + ' ' +
               this.section.section_id);
    },
  },
};
</script>
