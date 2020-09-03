<template>
  <div>
    <div class="mb-4 schedule-body">
      <div class="time-column myuw-text-xs" aria-hidden="true">
        <div v-for="(time, i) in timeSlots" :key="i"
             class="time-cell"
        >
          <div v-if="time.minute() == 0" class="font-weight-bold text-nowrap">
            {{ time.format('ha') }}
          </div>
          <div v-else class="d-none">
            {{ time.format('h:mma') }}
          </div>
        </div>
      </div>
      <!-- Desktop Version -->
      <div v-if="$mq !== 'mobile'" class="d-flex w-100">
        <div v-for="day in daySlots" :key="day"
             :aria-labelledby="`${day}-${period.id}`"
             role="group"
             class="day-column"
        >
          <div class="font-weight-bold text-center myuw-text-xs day-heading">
            <div :id="`${day}-${period.id}`">
              {{ days[day] }}
              <span v-if="isFinalsTab" class="d-block">
                {{ getFirstFinalExamTimeOn(day).format('MMM D') }}
              </span>
            </div>
          </div>
          <div v-for="(time, i) in timeSlots" :key="i"
               :class="{'day-cell': true, 'day-disabled': isDayDisabled(day)}"
          >
            <div v-if="(
              meetingMap[day][formatToUnique(time)] &&
              meetingMap[day][formatToUnique(time)].length > 0
            )" class="d-flex"
            >
              <uw-course-section
                v-for="(meetingData, j) in
                  meetingMap[day][formatToUnique(time)]"
                :key="j" :meeting-data="meetingData"
                :is-finals-card="isFinalsTab"
              />
            </div>
          </div>
        </div>
      </div>
      <!-- Mobile Version -->
      <div v-else class="w-100">
        <div class="mobile-column-selector">
          <b-form-select
            v-model="mobile['current']"
            aria-label="Select the Day of Week:"
            :options="mobile['options']"
            class="font-weight-bold myuw-text-md"
          />
        </div>
        <div class="day-column">
          <div class="mobile-column-selector">
            <b-form-select
              v-model="mobile['current']"
              aria-label="Select the Day of Week:"
              :options="mobile['options']"
              class="font-weight-bold myuw-text-md"
            />
          </div>
          <div v-for="(time, i) in timeSlots" :key="i" class="day-cell">
            <div v-if="(
              meetingMap[mobile['current']][formatToUnique(time)] &&
              meetingMap[mobile['current']][formatToUnique(time)].length > 0
            )" class="d-flex"
            >
              <uw-course-section
                v-for="(meetingData, j) in
                  meetingMap[mobile['current']][formatToUnique(time)]"
                :key="j" :meeting-data="meetingData"
                :is-finals-card="isFinalsTab"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- TODO: move eos data here -->
    <div>
      <p class="text-muted myuw-text-md">
        BIGDATA 230 A, meeting time updates:
      </p>
      <ol class="myuw-text-md">
        <li>Apr 3 – Jun 12 (6:00 – 9:00PM)</li>
        <li>May 11 – May 15 (Class does not meet)</li>
        <li>May 29 (Class does not meet)</li>
      </ol>
    </div>

    <div v-if="meetingsWithoutTime.length > 0">
      <p v-if="!isFinalsTab" class="text-muted myuw-text-md">
        No meeting time specified:
      </p>
      <p v-else class="text-muted myuw-text-md">
        Courses with final exam meeting times to be determined or courses with
        no final exam:
      </p>
      <div v-for="(meeting, i) in meetingsWithoutTime" :key="i"
           class="d-inline-block w-25 mr-2"
      >
        <uw-course-section :meeting-data="meeting" />
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';
import CourseSection from './course-section.vue';

export default {
  components: {
    'uw-course-section': CourseSection,
  },
  props: {
    period: {
      type: Object,
      required: true,
    },
  },
  data: function() {
    return {
      days: {
        monday: 'MON',
        tuesday: 'TUE',
        wednesday: 'WED',
        thursday: 'THU',
        friday: 'FRI',
        saturday: 'SAT',
        sunday: 'SUN',
      },
      timestep: [30, 'minutes'],
      timeSlots: [],
      daySlots: [],
      meetingMap: {},
      meetingsWithoutTime: [],
      hasMeetingsWithTime: false,
      isFinalsTab: false,
      mobile: {
        current: null,
        options: [],
      },
    };
  },
  created() {
    // Set if this tab is for finals
    this.isFinalsTab = this.period.id == 'finals';

    // If there are no meetings with defined time in this period
    if (
      !(
        this.period.earliestMeetingTime == null &&
        this.period.latestMeetingTime == null
      )
    ) {
      // Initialize the rendering logic
      this.initializeTimeSlots();
      this.initializeDaySlots();
      this.initializeMeetingMap();

      // Put in the meeting with time into the map.
      this.period.sections.forEach((section) => {
        if (!this.isFinalsTab) {
          section.meetings.forEach((meeting) => {
            if (meeting.start_time && meeting.end_time) {
              for (const day in meeting.meeting_days) {
                if (meeting.meeting_days[day]) {
                  this.putMeeting(
                      section,
                      meeting,
                      meeting.start_time,
                      day,
                  );
                  this.hasMeetingsWithTime = true;
                }
              }
            }
          });
        } else {
          if (
            section.final_exam &&
            section.final_exam.start_date &&
            section.final_exam.end_date
          ) {
            this.putMeeting(
                section,
                section.final_exam,
                section.final_exam.start_date,
                section.final_exam.start_date.format('dddd').toLowerCase(),
            );
            this.hasMeetingsWithTime = true;
          }
        }
      });
    }

    // Put the meeting without time into its list.
    this.period.sections.forEach((section) => {
      if (!this.isFinalsTab) {
        section.meetings.forEach((meeting) => {
          if (!(meeting.start_time && meeting.end_time)) {
            this.meetingsWithoutTime.push({
              section: section,
              meeting: meeting,
            });
          }
        });
      } else {
        if (
          !(
            section.final_exam &&
            section.final_exam.start_date &&
            section.final_exam.end_date
          )
        ) {
          this.meetingsWithoutTime.push({
            section: section,
            meeting: section.final_exam,
          });
        }
      }
    });

    this.initializeMobileDaySlots();
  },
  methods: {
    // Converts a moment object to a standard string that is used in timeslots
    formatToUnique(t) {
      return t.format('hh:mm A');
    },
    // Returns minutes from midnight
    getMFM(t) {
      return (t.hour() * 60) + t.minute();
    },
    // Puts a meeting in meetingMap at time startTime and calculates variables
    // needed to render the meetingMap.
    putMeeting(section, meeting, startTime, day) {
      let meetingsToAdd = [{
        section: section,
        meeting: meeting,
      }];

      if (
        this.meetingMap[day][this.formatToUnique(startTime)] &&
        this.meetingMap[day][this.formatToUnique(startTime)].length > 0
      ) {
        meetingsToAdd = meetingsToAdd.concat(
            this.meetingMap[day][this.formatToUnique(startTime)],
        );
      }

      this.meetingMap[day][this.formatToUnique(startTime)] = meetingsToAdd;
    },
    getFirstFinalExamTimeOn(day) {
      return this.period.latestMeetingTime.day(
          day.replace(/^([a-z])/, (c) => c.toUpperCase()),
      );
    },
    isDayDisabled(day) {
      return this.period.disabled_days && this.period.disabled_days[day];
    },
    // -- Some helper functions to initalize the state. --
    // Make a array of all the possible time slots with the interval
    // of this.timestep
    initializeTimeSlots() {
      let start = this.period.earliestMeetingTime.clone()
          .subtract(...this.timestep);
      let end = this.period.latestMeetingTime.clone().add(...this.timestep);
      if (!(end.minute() === 30 || end.minute() === 0)) {
        end = end.add(10, 'minutes');
      }

      while (start.format('hh:mm A') !== end.format('hh:mm A')) {
        this.timeSlots.push(start.clone());

        start = start.add(...this.timestep);
      }
      this.timeSlots.push(start.clone());
    },
    // Setting the days of the week that need to be displayed
    initializeDaySlots() {
      this.daySlots = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'];
      if (this.period.meets_saturday) {
        this.daySlots.push('saturday');
      }
      if (this.period.meets_sunday) {
        this.daySlots.unshift('sunday');
      }
    },
    // Initalizes the mobile values for days needs to be called
    // at the end of create
    initializeMobileDaySlots() {
      this.daySlots.forEach((day) => {
        const i = this.mobile['options'].push({
          value: day,
          text: day.replace(/^([a-z])/, (c) => c.toUpperCase()),
        });
        if (this.isFinalsTab) {
          this.mobile['options'][i - 1].text += (
            ' - ' + this.getFirstFinalExamTimeOn(day).format('MMMM D')
          );
        }

        let hasMeetingToday = false;
        this.timeSlots.forEach((time) => {
          if (
            this.meetingMap[day][this.formatToUnique(time)] &&
            this.meetingMap[day][this.formatToUnique(time)].length > 0
          ) {
            hasMeetingToday = true;
          }
        });

        if (!hasMeetingToday) {
          this.mobile['options'][i - 1].text += ` (no ${
            this.isFinalsTab ? 'finals' : 'sections'
          } scheduled)`;
          this.mobile['options'][i - 1].disabled = true;
        }
      });
      if (this.isFinalsTab) {
        this.mobile['current'] = this.daySlots[0];
      } else {
        this.mobile['current'] = moment().format('dddd').toLowerCase();
      }
    },
    // Initalize the meeting map.
    initializeMeetingMap() {
      this.daySlots.forEach((daySlot) => {
        this.meetingMap[daySlot] = {};
        this.timeSlots.forEach((timeSlot) => {
          this.meetingMap[daySlot][this.formatToUnique(timeSlot)] = [];
        });
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@import "../../../../css/custom.scss";

$heading-height: 45px;
$cell-height: 30px;

.schedule-body {
  width: 100%;
  display: flex;
}
.time-column {
  padding-top: $heading-height - ($cell-height / 2) ;
  height: 100%;
  flex-basis: 45px;
  display: flex;
  flex-direction: column;

  .time-cell {
    flex-grow: 1;
    height: $cell-height;
    position: relative;

    div {
      position: absolute;
      top: 50%; left: 50%;
      transform: translate(-50%,-50%);
      width: 100%;
      text-align: center;
    }
  }
}
.day-column {
  height: 100%;
  flex-grow: 1;
  flex-basis: 0;

  .day-heading {
    height: $heading-height;
    position: relative;

    div {
      position: absolute;
      top: 50%; left: 50%;
      transform: translate(-50%,-50%);
      width: 100%;
    }
  }

  .day-cell {
    height: $cell-height;

    // Border logic for empty cells
    // &:empty {
      &:nth-child(even) {
        border-top: 1px solid darken($table-border-color, 5%);

        &:last-child {
          border-bottom: 1px dashed darken($table-border-color, 5%);
        }
      }

      &:nth-child(odd) {
        border-top: 1px dashed darken($table-border-color, 5%);

        &:last-child {
          border-bottom: 1px solid darken($table-border-color, 5%);
        }
      }
    // }
    border-left: 1px solid darken($table-border-color, 5%);
  }

  .day-disabled {
    background-color: #dedede;
  }

  &:last-child {
    .day-cell {
      border-right: 1px solid darken($table-border-color, 5%);
    }
  }
}
.mobile-column-selector {
  height: $heading-height;
}
</style>
