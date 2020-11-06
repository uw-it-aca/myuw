<template>
  <div v-if="evalData.length > 0" class="d-flex">
    <h5
      :class="[!showRowHeading ? 'sr-only' : '']"
      class="w-25 font-weight-bold myuw-text-md"
    >
      Course Evaluations
    </h5>
    <div class="w-75 myuw-text-md">
      <div
        v-for="(evalObj, idx) in evalData"
        :key="`${section.id}-eval-${idx}`"
        class="mb-3 myuw-eval-list"
      >
        <template v-if="evalObj.is_multi_instr">
          <!-- evaluation is on the course -->
          <p>
            <a :href="evalObj.url" target="_blank">
              {{ section.curriculum_abbr }}
              {{ section.course_number }}
              {{ section.section_id }}
              Evaluation
            </a>
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

          <p class="myuw-text-md m-0">
            Evaluations close
            <strong>{{ toFriendlyDate(evalData[idx].close_date) }}</strong>
            (at 11:59PM), and only take a few minutes to complete.
          </p>
        </template>
        <template v-else>
          <ul class="list-unstyled myuw-text-md mb-0">
            <li v-for="(instructor, index) in evalObj.instructors"
                :key="`${section.id}-eval-inst-${index}`"
                class="mb-0"
            >
              <a :href="evalObj.url" target="_blank">
                {{ titleCaseName(instructor.instructor_name) }}
              </a>
              <div v-if="hasTitle(instructor)"
                   class="font-italic text-muted mb-2"
              >
                {{ instructor.instructor_title }}
              </div>
              <p class="myuw-text-md m-0">
                Evaluations close
                <strong>{{ toFriendlyDate(evalData[idx].close_date) }}</strong>
                (at 11:59PM), and only take a few minutes to complete.
              </p>
            </li>
          </ul>
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
.myuw-eval-list {
  &:last-child {
    margin-bottom: 0 !important;
  }
}
</style>
