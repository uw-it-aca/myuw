<template>
  <a
    role="button"
    :class="selector.toLowerCase()"
    data-bs-container="body"
    data-bs-toggle="popover"
    :title="title"
    data-bs-placement="bottom"
    data-bs-html="true"
    :data-bs-content="content"
  >
    <font-awesome-icon :icon="faQuestionCircle" class="text-dark-gray" />
  </a>
</template>

<script>
import { faQuestionCircle } from '@fortawesome/free-solid-svg-icons';
import { Popover } from 'bootstrap';
export default {
  props: {
    selector: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    content: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      faQuestionCircle,
    };
  },
  mounted() {
    var popover = new Popover(document.querySelector(
      "." + this.selector.toLowerCase()));
  },
};
</script>

<style lang="scss" scoped>
@use 'sass:map';
@import '../../../myuw/static/css/myuw/variables.scss';
</style>
