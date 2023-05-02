<template>
  <div>
    <ul class="list-unstyled mb-0">
      <template v-for="(termMajor, index) in termMajors">
        <li v-if="index == 0" :key="index" class="mb-1">
          {{ degreeListString(termMajor.majors) }}
        </li>
        <li v-else-if="termMajor.degrees_modified" :key="index" class="mb-1">
          Beginning {{ titleCaseWord(termMajor.quarter) }} {{ termMajor.year }}:
          &nbsp;&nbsp;
          <span v-if="termMajor.majors.length > 0">
            {{ degreeListString(termMajor.majors) }}
          </span>
          <span v-else class="text-muted">
            None
          </span>
        </li>
      </template>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    termMajors: {
      type: Array,
      required: true,
    },
  },
};
</script>
