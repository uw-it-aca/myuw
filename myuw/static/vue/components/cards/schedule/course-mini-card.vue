<template>
  <div>
    <div v-for="(meetingData, i) in meetings" :key="i" role="group"
         tabindex="0" style="background-color: #e8e3d3"
    >
      <abbr v-if="meetingData.section.is_teaching" title="Teaching Course">
        T
      </abbr>
      <div :class="`bg-c${meetingData.section.color_id}`">
        <a :href="sectionUrl(meetingData.section)">
          {{sectionTitle(meetingData.section)}}
        </a>
      </div>
      <a v-if="showConfirmLink(meetingData.section)"
         :href="confirmationLink(meetingData.section)"
         target="_blank">
        (Confirm)
      </a>
      <div>
        <a v-if="(
          !meetingData.section.is_remote &&
           meetingLocationUrl(meetingData.meeting)
          )"
          :href="meetingLocationUrl(meetingData.meeting)"
        >
          {{meetingLocation(meetingData.section, meetingData.meeting)}}
        </a>
        <span v-else>
          {{meetingLocation(meetingData.section, meetingData.meeting)}}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import {mapState} from 'vuex';

export default {
  props: {
    meetings: {
      type: Array,
      required: true,
    },
    isFinalsCard: {
      type: Boolean,
      default: false,
    }
  },
  computed: {
    ...mapState({
      netid: (state) => state.user.netid,
      quarter: (state) => state.termData.quarter.replace(
        /^([a-z])/, (c) => c.toUpperCase()
      ),
      year: (state) => state.termData.year,
    }),
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
    meetingLocation: function(section, meeting) {
      if (section.is_remote) {
        return "Remote";
      }
      if (meeting != null && meeting.no_meeting) {
        return "No Meeting";
      }
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
        return `http://maps.google.com/maps?q=${
          meeting.latitude
        },${meeting.longitude}+(${meeting.building})&z=18`;
      }
      return false;
    },
    showConfirmLink: function(section) {
      return (
        section.is_teaching &&
        this.isFinalsCard &&
        !section.final_exam.no_exam_or_nontraditional &&
        !section.final_exam.is_confirmed
      );
    },
    confirmationLink: function(section) {
      return `https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/${
        this.netid
      }/finalexam.asp?${this.quarter}+${this.year}&sln=${section.sln}`;
    }
  }
}
</script>