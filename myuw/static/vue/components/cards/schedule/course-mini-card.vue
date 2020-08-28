<template>
  <div>
    <div v-for="(meetingData, i) in meetings" :key="i" role="group"
         tabindex="0" style="background-color: #e8e3d3"
    >
      <div :class="`bg-c${meetingData.section.color_id}`">
        <a :href="sectionUrl(meetingData.section)">
          {{sectionTitle(meetingData.section)}}
        </a>
      </div>
      <div>
        <a v-if="meetingLocationUrl(meetingData.meeting)"
          :href="meetingLocationUrl(meetingData.meeting)"
        >
          {{meetingLocation(meetingData.meeting)}}
        </a>
        <span v-else>
          {{meetingLocation(meetingData.meeting)}}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    meetings: {
      type: Array,
      required: true,
    },
  },
  methods: {
    sectionTitle: function(section) {
      return `${section.curriculum_abbr} ${section.course_number} ${section.section_id}`;
    },
    sectionUrl: function(section) {
      return `/academics/#${section.curriculum_abbr}-${section.course_number}-${section.section_id}`;
    },
    isRoomTBD: function(meeting) {
      return meeting == null || (meeting.room_tbd || !(
        'building' in meeting && meeting.building != '*' &&
        'room' in meeting && meeting.room != '*'
      ));
    },
    meetingLocation: function(meeting) {
      if (!this.isRoomTBD(meeting)) {
        return `${meeting.building} ${meeting.room}`
      }
      return "Room TBD";
    },
    meetingLocationUrl: function(meeting) {
      if (
        !this.isRoomTBD(meeting) &&
        'latitude' in meeting &&
        'longitude' in meeting
      ) {
        return `http://maps.google.com/maps?q=${meeting.latitude},${meeting.longitude}+(${meeting.building})&z=18`;
      }
      return false;
    }
  }
}
</script>