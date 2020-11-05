<template>
  <div v-if="evalData.length > 0" class="d-flex">
    <h5
      :class="[!showRowHeading ? 'sr-only' : '']"
      class="w-25 font-weight-bold myuw-text-md"
    >
      Course Evaluations
    </h5>
    <div class="w-75">
      <div
        v-for="(evalObj, idx) in evalData"
        :key="`${section.id}-eval-${idx}`"
      >
        <template v-if="evalObj.is_multi_instr">
          <!-- evaluation is on the course -->
          <a :href="evalObj.url" target="_blank">
            {{ section.curriculum_abbr }}
            {{ section.course_number }}
            {{ section.section_id }}
            Evaluation
          </a>
          <p class="myuw-text-md">
            <strong>Evaluations close
              {{ toFriendlyDate(evalData[idx].close_date) }}</strong>
            (at 11:59PM), and only take a few minutes to complete.
          </p>
          <ul class="list-unstyled myuw-text-md mb-0">
            <li
              v-for="(instructor, index) in evalObj.instructors"
              :key="`${section.id}-eval-inst-${index}`"
          >
            {{ titleCaseName(instructor.instructor_name) }}
            <span v-if="hasTitle(instructor)">
              {{ instructor.instructor_title }}
            </span>
          </li>
        </ul>
      </template>
      <template v-else>
        <ul>
          <li v-for="(instructor, index) in evalObj.instructors"
              :key="`${section.id}-eval-inst-${index}`"
          >
            <a :href="evalObj.url" target="_blank">
              {{ titleCaseName(instructor.instructor_name) }}
            </a>
            <span v-if="hasTitle(instructor)">
              {{ instructor.instructor_title }}
            </span>
          </li>
        </ul>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    evalData: {
      type: Array,
      required: true,
    },
    section: {
      type: Object,
      required: true,
    },
    showRowHeading: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    hasTitle(instructor) {
      return (instructor.instructor_title &&
       instructor.instructor_title.length > 0);
    },
  },
};
</script>

<style lang="scss" scoped>
li:last-child { margin-bottom: 0 !important;}
</style>
