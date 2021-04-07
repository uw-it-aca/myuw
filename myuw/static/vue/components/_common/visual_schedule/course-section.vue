<template>
  <div class="course-section flex-fill" :style="computedStyles">
    <div
      role="group"
      tabindex="0"
      class="course-section-inner"
    >
      <div :class="`bg-c${meetingData.section.color_id}`"
           class="p-1 text-center myuw-text-xxs"
      >
        <b-badge v-if="meetingData.section.is_teaching" variant="light">
          <abbr title="Teaching Course">T</abbr>
        </b-badge>
        <a :href="sectionUrl" class="text-white">
          {{ sectionTitle }}
        </a>
      </div>

      <div class="p-1 text-center myuw-text-xxs">
        <slot>
          <a v-if="(
               !meetingData.section.is_remote &&
               meetingLocationUrl
             )"
             v-out="ariaMeetingLocation"
             :href="meetingLocationUrl"
          >
            {{ meetingLocation }}
          </a>
          <span v-else>
            {{ meetingLocation }}
          </span>
          <a v-if="showConfirmLink"
            v-out="'Confirm Meeting'"
            :href="confirmationLink"
            class="d-block"
          >
            (Confirm)
          </a>
        </slot>
      </div>
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
    day: {
      type: String,
      default: null,
    },
    term: {
      type: Object,
      required: true,
    },
  },
  computed: {
    ...mapState({
      netid: (state) => state.user.netid,
    }),
    quarter() {
      return this.titleCaseWord(this.term.quarter);
    },
    year() {
      return this.term.year;
    },
    computedStyles: function() {
      if (this.meetingData.meeting && !this.meetingData.meeting.no_meeting) {
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
            'height': `${(this.getMFM(endTime) - this.getMFM(startTime))*35/30}px`,
            'margin-top': `${
              startTime.minute() -
              (this.meetingData.renderTime.minute() + 1)
            }px`,
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
      let page = this.meetingData.section.is_teaching ? 'teaching' : 'academics';
      let term = this.meetingData.section.is_teaching
        ? this.year + ',' + this.quarter.toLowerCase() : '';
      return `/${page}/${term}#${
        this.meetingData.section.curriculum_abbr
      }-${
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
        return 'No meeting';
      }
      if (!this.isRoomTBD()) {
        return `${
          this.meetingData.meeting.building
        } ${this.meetingData.meeting.room}`;
      }
      return 'Room TBD';
    },
    ariaMeetingLocation: function() {
      if (this.meetingData.section.is_remote) {
        return 'Location: Remote';
      }
      if (
        this.meetingData.meeting != null &&
        this.meetingData.meeting.no_meeting
      ) {
        return 'Location: None';
      }
      if (!this.isRoomTBD()) {
        return `Building: ${
          this.meetingData.meeting.building
        } Room: ${this.meetingData.meeting.room}`;
      }
      return 'Location: Room TBD';
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

        label += 'Meeting time: ';

        if (this.day) {
          label += `${this.titleCaseWord(this.day)}, `;
        }

        if (startTime && endTime) {
          label += `${
            startTime.format('h:mma')
          }-${endTime.format('h:mma')}`;
        }

        if (!this.day && !startTime && !endTime) {
          label += 'None';
        }
      }

      // label += `${this.sectionTitle}, ${this.ariaMeetingLocation}`;

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
@use "sass:map";
@import "../../../../css/myuw/variables.scss";

.course-section {
  width: 100%;
  position: relative;
  overflow: hidden;

  .course-section-inner {
    background-color: lighten(map.get($theme-colors, "beige"), 7%) !important;
    height: 100%;
    overflow: hidden;
  }

  &:not(:last-child) {
    border-right: solid 1px transparent;
  }

  &:focus, &:focus-within, &:hover {
    z-index:9999;
    flex-shrink: 0.3 !important;
    outline: 2px solid $link-color;
    border: 0;
    /*
    & + .course-section {
      border: 0;
    }*/
  }
}
</style>
