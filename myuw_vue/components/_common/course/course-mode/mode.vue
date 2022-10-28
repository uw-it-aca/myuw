<template>
  <div class="text-uppercase myuw-text-sm">
    <span v-if="section.is_asynchronous">
      Asynchronous Online (A)
    </span>
    <span v-else-if="section.is_synchronous">
      Synchronous Online (O)
    </span>
    <span v-else-if="section.is_hybrid">
      Hybrid (B)
    </span>
    <span v-else>
      In Person
    </span>
    <a
      v-if="!hideInfoLink"
      v-out="'course-mode'"
      href="https://registrar.washington.edu/classrooms/course-modes/"
      :title="title"
    ><font-awesome-icon :icon="faQuestionCircle" /></a>
  </div>
</template>

<script>
import {
  faQuestionCircle,
} from '@fortawesome/free-solid-svg-icons';
export default {
  props: {
    section: {
      type: Object,
      required: true,
    },
    hideInfoLink: {
      type: Boolean,
      default: false,
    },
    includeTSC: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      faQuestionCircle,
    }
  },
  computed: {
    title() {
      return (
        this.includeTSC ?
        "Learn About Course Mode, in case of an error please" +
        "contact your department Time Schedule coordinator." :
        "Learn About Course Mode");
    },
  },
};
</script>
