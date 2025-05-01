<template>
  <li v-if="index == 0" class="mb-1" :key="index">
    <span :id="`major-${index}}`">
      {{ degreeListString(termMajor.majors) }}
    </span>
    <span v-if="invalid_degree_name">
      <font-awesome-icon :icon="faExclamationTriangle" class="me-1" />
      <uw-tooltip :target="`major-${index}}`" :title="tooltipMessage" />
    </span>
  </li>
  <li v-else-if="termMajor.degrees_modified" class="mb-1" :key="index">
    Beginning {{ titleCaseWord(termMajor.quarter) }} {{ termMajor.year }}:
    &nbsp;&nbsp;
    <span v-if="termMajor.majors.length > 0" :id="`major-${index}}`">
      {{ degreeListString(termMajor.majors) }}
    </span>
    <span v-if="invalid_degree_name">
      <font-awesome-icon :icon="faExclamationTriangle" class="me-1" />
      <uw-tooltip :target="`major-${index}}`" :title="tooltipMessage" />
    </span>
  </li>
</template>

<script>
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';
import Tooltip from '../../_templates/tooltip.vue';

export default {
  components: {
    'uw-tooltip': Tooltip,
  },
  data() {
    return {
      faExclamationTriangle,
    };
  },
  props: {
    index: {
      type: Number,
      required: true,
    },
    termMajor: {
      type: Object,
      required: true
    },
  },
  computed: {
    invalid_degree_name () {
      if (this.termMajor.majors.length == 0) return false;
      const major = this.termMajor.majors[0];
      return major.name === null && major.college_abbr.length > 0 && major.degree_level > 0;
    },
    tooltipMessage() {
      return (
        "The major name that you have used is no longer valid. " +
        "Please contact your department to update your major(s)."
      );
    }
  },
};
</script>
