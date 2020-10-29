<template>
  <div v-if="evalData && evalData.length > 0">
    <h5>Course Evaluations</h5>
    <p>
      <span>Evaluations close {{ toFriendlyDate(eval.close_date) }}</span>
      (at 11:59PM), and only take a few minutes to complete.
    </p>

    <div v-for="(eval, index) in evalData"
      :key="`${section.id}-eval-${index}`">
      <template v-if="eval.is_multi_instr">
        <!-- evaluation is on the course -->
        <a :href="eval.url" target="_blank">
          {{ section.curriculum_abbr }} {{ section.course_number }} {{ section.section_id }} Evaluation</span>
        </a>
        <ul>
          <li v-for="(instructor, index) in eval.instructors"
            :key="`${section.id}-eval-inst-${index}`">
            <span>
              {{ instructor.instructor_name }}
            </span>
            <span v-if="instructor.instructor_title.length > 0">
              {{ instructor.instructor_title }}
            </span>
          </li>
        </ul>
      </template>
      <template v-else>
        <ul>
          <li v-for="(instructor, index) in eval.instructors"
            :key="`${section.id}-eval-inst-${index}`">
            <a :href="eval.url" target="_blank">
              {{ titleCaseName(instructor.dinstructor_name) }}
            </a>
            <span v-if="instructor.instructor_title.length > 0">
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
  },
  methods: {
    titleCaseName(str) {
      return str.split(' ').map(function(w) {
        return w[0].toUpperCase() + w.substr(1).toLowerCase();
      }).join(' ');
    },
  },
};
</script>
