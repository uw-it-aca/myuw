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
        <span v-if="meetingData.section.is_teaching" class="badge bg-light text-dark">
          <abbr title="Teaching Course">T</abbr>
        </span>
        <a :href="sectionUrl" class="text-white">
          {{ sectionTitle }}
        </a>
      </div>

      <div class="p-1 text-center myuw-text-xxs">
        <slot>
          <a v-if="meetingLocationUrl"
             v-out="ariaMeetingLocation"
             :href="meetingLocationUrl"
             :title="`Map of ${meetingData.meeting.building_name}`"
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
    isFinalsTab: {
      type: Boolean,
      required: true,
    },
    day: {
      type: String,
      default: null,
    },
    term: {
      type: Object,
      required: true,
    },
    meetingsWithoutTime: {
      type: Boolean,
      required: false,
    },
  },
  computed: {
    quarter() {
      return this.titleCaseWord(this.term.quarter);
    },
    year() {
      return this.term.year;
    },
    computedStyles() {
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
    sectionTitle() {
      return `${this.meetingData.section.curriculum_abbr} ${
        this.meetingData.section.course_number
      } ${this.meetingData.section.section_id}`;
    },
    sectionUrl() {
      let page = (
        this.meetingData.section.is_teaching ? 'teaching' : (
        this.term.isNotCurrentTerm ? 'future_quarters' :'academics'));
      let tm = this.meetingData.section.is_teaching ?
        this.year + ',' + this.quarter.toLowerCase() :
        (this.term.isNotCurrentTerm ? this.term.termLabel : '');
      return `/${page}/${tm}#${
        this.meetingData.section.curriculum_abbr.replace(/ /g, '-')
      }-${
        this.meetingData.section.course_number
      }-${this.meetingData.section.section_id}`;
    },
    isInPerson() {  // MUWM-5099
      return (
        this.meetingData.section &&
        !(this.meetingData.section.is_asynchronous ||
          this.meetingData.section.is_synchronous ||
          this.meetingData.section.is_hybrid));
    },
    wontMeet() {
      return (
        !this.meetingData.meeting ||
        this.meetingData.meeting.wont_meet
      );
    },
    hasBuildingRoom() {
      return (
        this.meetingData.meeting &&
        'building' in this.meetingData.meeting && this.meetingData.meeting.building != '*' &&
        'room' in this.meetingData.meeting && this.meetingData.meeting.room != '*'
      );
    },
    meetingLocation() {
      if (this.meetingsWithoutTime || this.wontMeet) {
        // MUWM-5208
        if (this.isFinalsTab) {
          return '';
        }
        if (!this.isInPerson) {
          return 'Online';
        }
        return '';
      }
      if (this.hasBuildingRoom) {
        return `${
          this.meetingData.meeting.building
        } ${this.meetingData.meeting.room}`;
      }
      if (!this.isInPerson) {
        // MUWM-5208
        if (!this.isFinalsTab) {
          return 'Online';
        }
        return 'TBD';
      }
      return 'Room TBD';
    },
    ariaMeetingLocation() {
      if (this.meetingsWithoutTime || this.wontMeet) {
        // MUWM-5208
        if (this.isFinalsTab) {
          return 'Location: None';
        }
        if (!this.isInPerson) {
          return 'Location: Online';
        }
        return 'Location: None';
      }
      if (this.hasBuildingRoom) {
        return `${
          this.meetingData.meeting.building
        } ${this.meetingData.meeting.room}`;
      }
      if (!this.isInPerson && !this.isFinalsTab) {
        // MUWM-5208
        return 'Location: Online';
      }
      return 'Location: TBD';
    },
    meetingLocationUrl() {
      if (this.hasBuildingRoom &&
          'latitude' in this.meetingData.meeting &&
          'longitude' in this.meetingData.meeting
      ) {
        return `https://maps.google.com/maps?q=${
          this.meetingData.meeting.latitude
        },${this.meetingData.meeting.longitude}+(${
          this.meetingData.meeting.building
        })&z=18`;
      }
      return false;
    },
    showConfirmLink() {
      return (
        this.meetingData.section.is_teaching &&
        this.isFinalsTab &&
        this.meetingData.section.is_primary_section &&
        this.meetingData.section.final_exam &&
        !this.meetingData.section.final_exam.no_exam_or_nontraditional &&
        !this.meetingData.section.final_exam.is_confirmed
      );
    },
    confirmationLink() {
      // MUWM-5145
      return `https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/pop/finalexam.aspx?${
        this.quarter}+${this.year}&sln=${this.meetingData.section.sln}`;
    },
    ariaLabel() {
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
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import '../../../../myuw/static/css/myuw/variables.scss';

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
    border-end: solid 1px transparent;
  }

  &:focus, &:focus-within, &:hover {
    z-index:9999;
    flex-shrink: 0.3 !important;
    outline: 1px solid lightgray;
    border: 0;
    /*
    & + .course-section {
      border: 0;
    }*/
  }
}
</style>
