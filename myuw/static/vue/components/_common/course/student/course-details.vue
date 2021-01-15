<template>
  <div>
    <uw-meeting-info
      :section="section"
    />
    <uw-resources
      :section="section"
      :course="course"
    />
    <uw-instructors
      v-if="section.is_ended && section.instructors.length > 0"
      :instructors="section.instructors"
    />
  </div>
</template>

<script>
import MeetingInfo from '../meeting/schedule.vue';
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
  },
};
</script>
