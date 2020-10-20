<template>
  <div>
    <div class="mb-4 d-flex">
      <div class="flex-shrink-1 myuw-text-xs"
           aria-hidden="true"
      >
        <div class="d-flex flex-column time-column">
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
      </div>
      <!-- Desktop Version -->
      <div v-if="$mq !== 'mobile'"
           class="w-100"
      >
        <div class="d-flex flex-wrap">
          <div v-for="day in Object.keys(period.daySlots)" :key="day"
               :aria-labelledby="`${day}-${period.id}`"
               role="group"
               class="day-column-desktop flex-even"
          >
            <div class="font-weight-bold text-center myuw-text-xs day-heading">
              <div :id="`${day}-${period.id}`">
                {{ days[day] }}
                <span v-if="isFinalsTab && period.daySlots[day]"
                      class="d-block"
                >
                  {{ period.daySlots[day].format('MMM D') }}
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
                  :is-finals-card="isFinalsTab" :day="day"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Mobile Version -->
      <div v-else class="w-100">
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
                :is-finals-card="isFinalsTab" :day="mobile['current']"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- eos message display -->
    <div v-if="period.eosData.length > 0 && !isFinalsTab" class="mb-2">
      <p class="text-muted myuw-text-md mb-1">
        Meeting time notes:
      </p>
      <uw-course-section
        v-for="(eosSection, i) in period.eosData" :key="i"
        :meeting-data="{section: eosSection}"
        :is-finals-card="false" class="d-inline-block w-auto mr-2"
      >
        <ol class="m-0 px-4 text-left">
          <li v-for="(meeting, j) in eosSection.meetings" :key="j">
            <span v-if="i !== 0">,&nbsp;</span>
            <span v-if="meeting.eos_start_date">
              {{ formatDate(meeting.eos_start_date) }}
              <span v-if="!meeting.start_end_same">
                &ndash; {{ formatDate(meeting.eos_end_date) }}
              </span>
            </span>
            <span v-if="meeting.wont_meet">
              (Class does not meet)
            </span>
            <span v-else-if="meeting.no_meeting">
              (Online learning)
            </span>
            <span v-else>
              <span v-if="meeting.start_time">
                ({{ formatTime(meeting.start_time) }} &ndash;
                {{ formatTime(meeting.end_time) }})
              </span>
            </span>
          </li>
        </ol>
      </uw-course-section>
    </div>

    <!-- no meeting specified notes -->
    <div v-if="meetingsWithoutTime.length > 0">
      <p v-if="!isFinalsTab" class="text-muted myuw-text-md mb-1">
        No meeting time specified:
      </p>
      <p v-else class="text-muted myuw-text-md mb-1">
        Courses with final exam meeting times to be determined or courses with
        no final exam:
      </p>
      <div v-for="(meeting, i) in meetingsWithoutTime" :key="i"
           class="d-inline-block w-auto mr-2"
      >
        <uw-course-section :meeting-data="meeting" />
      </div>
    </div>
  </div>
</template>

<script>
import dayjs from 'dayjs';
import {mapState} from 'vuex';
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
        sunday: 'SUN',
        monday: 'MON',
        tuesday: 'TUE',
        wednesday: 'WED',
        thursday: 'THU',
        friday: 'FRI',
        saturday: 'SAT',
      },
      timestep: [30, 'minutes'],
      timeSlots: [],
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
  computed: {
    ...mapState({
      quarterLastDate: (state) => dayjs(
          state.termData.lastDay, 'dddd, MMMM D, YYYY',
      ),
      today: (state) => dayjs(state.termData.today, 'dddd, MMMM D, YYYY'),
    }),
  },
  created() {
    // Set if this tab is for finals
    this.isFinalsTab = this.period.id == 'finals';
    if (!(
      this.period.earliestMeetingTime &&
      this.period.latestMeetingTime
    )) {
      if (this.isFinalsTab) {
        this.period.earliestMeetingTime = this.quarterLastDate
            .clone().day(8).hour(8).minute(30);
        this.period.latestMeetingTime = this.quarterLastDate
            .clone().day(8).hour(11).minute(50);

        const refrenceDate = this.period.earliestMeetingTime.clone();
        for (const day in this.period.daySlots) {
          if (!this.period.daySlots[day]) {
            if (day === 'saturday') {
              this.period.daySlots[day] = refrenceDate.clone().day(6);
            } else {
              this.period.daySlots[day] = refrenceDate.clone().day(
                  7 + Object.keys(this.days).indexOf(day),
              );
            }
          }
        }
      } else {
        this.period.earliestMeetingTime = this.today
            .clone().day(1).hour(8).minute(30);
        this.period.latestMeetingTime = this.today
            .clone().day(5).hour(11).minute(50);
      }
    }

    // If there are no meetings with defined time in this period
    if (!(
      this.period.earliestMeetingTime == null &&
        this.period.latestMeetingTime == null
    )) {
      // Initialize the rendering logic
      this.initializeTimeSlots();
      this.initializeMeetingMap();

      // Put in the meeting with time into the map.
      this.period.sections.forEach((section) => {
        if (!this.isFinalsTab) {
          section.meetings.forEach((meeting) => {
            if (
              !meeting.no_meeting &&
              meeting.start_time &&
              meeting.end_time
            ) {
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
          if (
            (
              meeting.no_meeting ||
              !(meeting.start_time && meeting.end_time)
            ) &&
            (
              !(
                meeting.eos_start_date &&
                meeting.eos_end_date
              ) ||
              (
                meeting.eos_start_date &&
                meeting.eos_end_date &&
                (
                  (
                    meeting.eos_start_date >= this.period.start_date &&
                    meeting.eos_start_date <= this.period.end_date
                  ) || (
                    meeting.eos_end_date >= this.period.start_date &&
                    meeting.eos_end_date <= this.period.end_date
                  )
                )
              )
            )
          ) {
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
    // Converts a dayjs object to a standard string that is used in timeslots
    formatToUnique(t) {
      return t.format('hh:mm A');
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
    isDayDisabled(day) {
      return this.period.disabled_days && this.period.disabled_days[day];
    },
    // -- Some helper functions to initalize the state. --
    // Make a array of all the possible time slots with the interval
    // of this.timestep
    initializeTimeSlots() {
      let start = this.period.earliestMeetingTime.clone();
      if (start.minute() === 30) {
        start = start.subtract(...this.timestep);
      } else if (start.minute() === 0) {
        start = start.subtract(...this.timestep).subtract(...this.timestep);
      }

      let end = this.period.latestMeetingTime.clone();
      if (end.minute() !== 0 && end.minute() !== 30) {
        end = end.add(30 - end.minute(), 'minutes');
      }

      while (start.format('hh:mm A') !== end.format('hh:mm A')) {
        this.timeSlots.push(start.clone());

        start = start.add(...this.timestep);
      }
      this.timeSlots.push(start.clone());
    },
    // Initalizes the mobile values for days needs to be called
    // at the end of create
    initializeMobileDaySlots() {
      Object.keys(this.period.daySlots).forEach((day) => {
        const i = this.mobile['options'].push({
          value: day,
          text: day.replace(/^([a-z])/, (c) => c.toUpperCase()),
        });
        if (this.isFinalsTab && this.period.daySlots[day]) {
          this.mobile['options'][i - 1].text += (
            ' - ' + this.period.daySlots[day].format('MMM D')
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
        }
      });
      if (this.isFinalsTab) {
        this.mobile['current'] = Object.keys(this.period.daySlots)[0];
      } else {
        const dayToday = dayjs().format('dddd').toLowerCase();
        if (dayToday in Object.keys(this.period.daySlots)) {
          this.mobile['current'] = dayToday;
        } else {
          this.mobile['current'] = Object.keys(this.period.daySlots)[0];
        }
      }
    },
    // Initalize the meeting map.
    initializeMeetingMap() {
      Object.keys(this.period.daySlots).forEach((daySlot) => {
        this.meetingMap[daySlot] = {};
        this.timeSlots.forEach((timeSlot) => {
          this.meetingMap[daySlot][this.formatToUnique(timeSlot)] = [];
        });
      });
    },
    formatDate: (d) => {
      return d.format('MMM D');
    },
    formatTime: (t) => {
      return t.format('h:mmA');
    },
  },
};
</script>

<style lang="scss" scoped>
@import "../../../../css/myuw/variables.scss";

$heading-height: 45px;
$cell-height: 35px;

.time-column {
  padding-top: $heading-height - ($cell-height / 2) ;
  height: 100%;
  min-width: 42px;

  .time-cell {
    //flex-grow: 1;
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
.day-column-desktop {
  min-width: 50px;
  //max-width: 20%;
}
.day-column, .day-column-desktop {
  height: 100%;

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
    border-left: 1px solid darken($table-border-color, 5%);

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
  }

  .day-disabled {
    background-color: lighten($table-border-color, 5%);
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
