<template>
  <b-container fluid class="px-0">
    <b-row no-gutters>
      <b-col v-if="showRowHeading" cols="3">
        Meetings
      </b-col>
      <uw-meeting-info :section="section" />
    </b-row>
    <b-row no-gutters>
      <b-col v-if="showRowHeading" cols="3">
        Resources
      </b-col>
      <uw-resources :section="section" :course="course" />
    </b-row>
    <b-row no-gutters>
      <b-col v-if="showRowHeading" cols="3">
        Instructors
      </b-col>
      <uw-instructor-info
        v-if="section.is_ended && section.instructors.length > 0"
        :instructors="section.instructors"
      />
    </b-row>
  </b-container>
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
