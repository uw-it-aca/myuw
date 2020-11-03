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
    <uw-instructor-info
      v-if="section.is_ended && section.instructors.length > 0"
      :instructors="section.instructors"
      :show-row-heading="true"
    />
  </div>
</template>

<script>
import MeetingInfo from './meeting-info.vue';
import Resources from './resources.vue';
import InstructorInfo from './instructor-info.vue';

export default {
  components: {
    'uw-meeting-info': MeetingInfo,
    'uw-resources': Resources,
    'uw-instructor-info': InstructorInfo,
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
