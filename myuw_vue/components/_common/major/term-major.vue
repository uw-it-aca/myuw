<template>
  <li v-if="index == 0" class="mb-1">
    {{ degreeListString(termMajor.majors) }}
    <span v-if="invalid_degree_name">
      <font-awesome-icon :id="`major-${index}}`" :icon="faExclamationTriangle" class="me-1" />
      <uw-tooltip :target="`major-${index}}`" :title="tooltipMessage" />
    </span>
  </li>
  <li v-else-if="termMajor.degrees_modified" class="mb-1">
    Beginning {{ titleCaseWord(termMajor.quarter) }} {{ termMajor.year }}:
    &nbsp;&nbsp;
    <span v-if="termMajor.majors.length > 0">
      {{ degreeListString(termMajor.majors) }}
    </span>
    <span v-if="invalid_degree_name">
      <font-awesome-icon :id="`major-${index}}`" :icon="faExclamationTriangle" class="me-1" />
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
  data() {
    return {
      faExclamationTriangle,
    };
  },
  computed: {
    // MUWM-5399
    invalid_degree_name () {
      if (this.termMajor.majors.length == 0) return false;
      const major = this.termMajor.majors[0];
      return major.name === null && major.college_abbr.length > 0 && major.degree_level > 0;
    },
    tooltipMessage() {
      return "Please contact your academic adviser to resolve this error.";
    }
  },
};
</script>
