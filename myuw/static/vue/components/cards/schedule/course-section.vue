<template>
  <div role="group"
       tabindex="0" class="course-section"
       :style="computedStyles"
       :aria-label="ariaLabel"
  >
    <div :class="`bg-c${meetingData.section.color_id}`"
         class="p-1 text-center myuw-text-xxs"
    >
      <b-badge v-if="meetingData.section.is_teaching" variant="light">
        <abbr title="Teaching Course">T</abbr>
      </b-badge>
      <a :href="sectionUrl"
         class="text-white"
      >
        {{ sectionTitle }}
      </a>
    </div>

    <div class="p-1 text-center myuw-text-xxs">
      <a v-if="(
           !meetingData.section.is_remote &&
           meetingLocationUrl
         )"
         :href="meetingLocationUrl"
      >
        {{ meetingLocation }}
      </a>
      <span v-else>
        {{ meetingLocation }}
      </span>
      <a v-if="showConfirmLink"
         :href="confirmationLink"
         target="_blank"
         class="d-block"
      >
        (Confirm)
      </a>
    </div>
  </div>
</template>

<script>
import {mapState} from 'vuex';

export default {
  props: {
    meetingData: {
      type: Object,
      required: true,
    },
    isFinalsCard: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapState({
      netid: (state) => state.user.netid,
      quarter: (state) => state.termData.quarter.replace(
          /^([a-z])/, (c) => c.toUpperCase(),
      ),
      year: (state) => state.termData.year,
    }),
    computedStyles: function() {
      if (this.meetingData.meeting) {
        const startTime = (
          this.meetingData.meeting.start_time ||
          this.meetingData.meeting.start_date
        );
        const endTime = (
          this.meetingData.meeting.end_time ||
          this.meetingData.meeting.end_date
        );

        if (startTime && endTime) {
          return {
            'height': `${this.getMFM(endTime) - this.getMFM(startTime)}px`,
            'margin-top': '-1px',
          };
        }
      }

      return {};
    },
    sectionTitle: function() {
      return `${this.meetingData.section.curriculum_abbr} ${
        this.meetingData.section.course_number
      } ${this.meetingData.section.section_id}`;
    },
    sectionUrl: function() {
      return `/academics/#${this.meetingData.section.curriculum_abbr}-${
        this.meetingData.section.course_number
      }-${this.meetingData.section.section_id}`;
    },
    meetingLocation: function() {
      if (this.meetingData.section.is_remote) {
        return 'Remote';
      }
      if (
        this.meetingData.meeting != null &&
        this.meetingData.meeting.no_meeting
      ) {
        return 'No Meeting';
      }
      if (!this.isRoomTBD()) {
        return `${
          this.meetingData.meeting.building
        } ${this.meetingData.meeting.room}`;
      }
      return 'Room TBD';
    },
    meetingLocationUrl: function() {
      if (
        !this.isRoomTBD() &&
        'latitude' in this.meetingData.meeting &&
        'longitude' in this.meetingData.meeting
      ) {
        return `http://maps.google.com/maps?q=${
          this.meetingData.meeting.latitude
        },${this.meetingData.meeting.longitude}+(${
          this.meetingData.meeting.building
        })&z=18`;
      }
      return false;
    },
    showConfirmLink: function() {
      return (
        this.meetingData.section.is_teaching &&
        this.isFinalsCard &&
        !this.meetingData.section.final_exam.no_exam_or_nontraditional &&
        !this.meetingData.section.final_exam.is_confirmed
      );
    },
    confirmationLink: function() {
      return `https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/${
        this.netid
      }/finalexam.asp?${this.quarter}+${
        this.year
      }&sln=${this.meetingData.section.sln}`;
    },
    ariaLabel: function() {
      let label = '';

      if (this.meetingData.meeting) {
        const startTime = (
          this.meetingData.meeting.start_time ||
          this.meetingData.meeting.start_date
        );
        const endTime = (
          this.meetingData.meeting.end_time ||
          this.meetingData.meeting.end_date
        );

        if (startTime && endTime) {
          label += `${startTime.format('dddd')}, ${
            startTime.format('h:mma')
          }-${endTime.format('h:mma')}, `;
        }
      }

      label += `${this.sectionTitle}, ${this.meetingLocation}`;

      return label;
    },
  },
  methods: {
    // Returns minutes from midnight
    getMFM(t) {
      return (t.hour() * 60) + t.minute();
    },
    isRoomTBD: function() {
      return (
        this.meetingData.meeting == null ||
        (
          this.meetingData.meeting.room_tbd ||
          !(
            'building' in this.meetingData.meeting &&
            this.meetingData.meeting.building != '*' &&
            'room' in this.meetingData.meeting &&
            this.meetingData.meeting.room != '*'
          )
        )
      );
    },
  },
};
</script>

<style lang="scss" scoped>
.course-section {
  background-color: lighten(#e8e3d3, 7%);;
  width: 100%;
  position: relative;
  outline: transparent auto 1px;
  overflow: hidden;
  margin-left: 2px;
  margin-right: 2px;

  &:hover {
    z-index:9999;
    outline-color: -webkit-focus-ring-color;
  }

  &:focus, &:focus-within {
    z-index:9999;
    outline-color: -webkit-focus-ring-color;
  }

}
</style>
