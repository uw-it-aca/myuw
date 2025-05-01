<template>
  <ul v-if="termMajors && termMajors.length > 0" class="list-unstyled mb-0">
    <template v-for="(termMajor, index) in termMajors">
      <major :index=index :term-major="termMajor" />
    </template>
  </ul>
  <span v-else class="text-muted">
    None
  </span>
</template>

<script>
import Major from './term_major.vue';
export default {
  components: {
    'major': Major,
  },
  props: {
    termMajors: {
      type: Array,
      default: () => [],
    },
  },
};
</script>