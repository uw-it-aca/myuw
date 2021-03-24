<template>
  <div v-if="evalData.length > 0">
    <h3 class="font-weight-bold myuw-text-md">
      Course Evaluations
    </h3>
    <div class="myuw-text-md">
      <div
        v-for="(evalObj, idx) in evalData"
        :key="`${section.id}-eval-${idx}`"
        class="mb-3 myuw-eval-list"
      >
        <template v-if="evalObj.is_multi_instr">
          <p>
            <a
              v-out="'Evaluate course'"
              :href="evalObj.url" target="_blank"
            >
              {{ section.curriculum_abbr }}
              {{ section.course_number }}
              {{ section.section_id }}
              Evaluation
            </a>
          </p>

          <!-- evaluation is on the course -->
          <p class="myuw-text-md m-0">
            <span>
              Evaluations close {{ toFriendlyDate(evalObj.close_date) }}
            </span>
            (at 11:59PM), and only take a few minutes to complete.
          </p>

          <ul class="list-unstyled myuw-text-md">
            <li
              v-for="(instructor, index) in evalObj.instructors"
              :key="`${section.id}-eval-inst-${index}`"
              class="mb-2"
            >
              <strong>{{ titleCaseName(instructor.instructor_name) }}</strong>
              <div v-if="hasTitle(instructor)" class="font-italic text-muted">
                {{ instructor.instructor_title }}
              </div>
            </li>
          </ul>
        </template>
        <template v-else>
          <ul class="list-unstyled myuw-text-md mb-0">
            <li v-for="(instructor, index) in evalObj.instructors"
                :key="`${section.id}-eval-inst-${index}`"
                class="mb-0"
            >
              <a
                v-out="'Evaluate instructor'"
                :href="evalObj.url" target="_blank">
                {{ titleCaseName(instructor.instructor_name) }}
              </a>
              <div v-if="hasTitle(instructor)"
                   class="font-italic text-muted mb-2"
              >
                {{ instructor.instructor_title }}
              </div>
            </li>
          </ul>
          <p class="myuw-text-md m-0">
            <span>
              Evaluations close {{ toFriendlyDate(evalObj.close_date) }}
            </span>
            (at 11:59PM), and only take a few minutes to complete.
          </p>
        </template>
      </div>
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
    hasTitle(instructor) {
      return (instructor.instructor_title &&
       instructor.instructor_title.length > 0);
    },
  },
};
</script>

<style lang="scss" scoped>
.myuw-eval-list {
  &:last-child {
    margin-bottom: 0 !important;
  }
}
</style>
