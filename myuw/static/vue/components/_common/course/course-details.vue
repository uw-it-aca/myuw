<template>
  <div>
    <uw-meeting-info
      :section="section"
      :show-row-heading="true"
    />
    <uw-resources
      :section="section"
      :course="course"
      :show-row-heading="true"
    />
    <uw-instructors
      v-if="section.is_ended && section.instructors.length > 0"
      :instructors="section.instructors"
      :show-row-heading="true"
    />
  </div>
</template>

<script>
import MeetingInfo from './meeting-info.vue';
import Resources from './resources.vue';
import Instructors from './instructors.vue';

export default {
  components: {
    'uw-meeting-info': MeetingInfo,
    'uw-resources': Resources,
    'uw-instructors': Instructors,
  },
  props: {
    course: {
      type: Object,
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
};
</script>
