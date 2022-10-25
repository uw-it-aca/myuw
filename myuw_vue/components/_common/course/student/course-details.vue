<template>
  <div>
    <h3 v-if="displayHeading"
      class="h6 text-dark-beige myuw-font-encode-sans"
    >
      Lecture Schedule
    </h3>
    <uw-course-mode :section="section"/>
    <uw-meeting-info :section="section"/>
    <uw-resources :section="section"/>

    <uw-instructors
      v-if="displayInstructor && section.instructors.length > 0"
      :instructors="section.instructors"
    />
  </div>
</template>

<script>
import MeetingInfo from '../meeting/schedule.vue';
import Modality from '../course-mode/modality.vue';
import Resources from './resources.vue';
import Instructors from './instructors.vue';

export default {
  components: {
    'uw-course-mode': Modality,
    'uw-meeting-info': MeetingInfo,
    'uw-resources': Resources,
    'uw-instructors': Instructors,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
    displayHeading: {
      type: Boolean,
      default: false,
    },
    displayInstructor: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
