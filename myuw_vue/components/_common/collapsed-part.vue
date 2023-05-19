<template>
  <span>
    <button
      v-uw-collapse="`${callerId}-${part.id}-collapse-${$meta.uid}`"
      v-no-track-collapse
      type="button"
      class="btn btn-link p-0 border-0 align-top notice-link text-start myuw-text-md"
    >
      <span class="notice-title" v-html="part.title" />
      <span v-if="displayOpenCloseIndicator">
        <font-awesome-icon v-if="!collapseOpen" :icon="faChevronDown" />
        <font-awesome-icon v-else :icon="faChevronUp" />
      </span>
    </button>
    <uw-collapse
      :id="`${callerId}-${part.id}-collapse-${$meta.uid}`"
      v-model="collapseOpen"
    >
      <div class="p-3 mt-2 bg-light text-dark notice-body myuw-text-md">
        <slot name="collapsed-body" />
      </div>
    </uw-collapse>
  </span>
</template>

<script>
import {
  faChevronUp,
  faChevronDown,
} from '@fortawesome/free-solid-svg-icons';
import Collapse from '../_templates/collapse.vue';
export default {
  components: {
    'uw-collapse': Collapse,
  },
  props: {
    callerId: {
      type: String,
      required: true,
    },
    part: {
      type: Object,
      required: true,
    },
    displayOpenCloseIndicator: {
      type: Boolean,
      default: false,
    },
  },
  data: function() {
    return {
      collapseOpen: false,
      faChevronUp,
      faChevronDown,
    };
  },
};
</script>
<style lang="scss" scoped>
@use "sass:map";
@import '../../../myuw/static/css/myuw/variables.scss';
</style>
