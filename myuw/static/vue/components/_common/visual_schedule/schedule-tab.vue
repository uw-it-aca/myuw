<template>
  <div>
    <div
      v-if="isSummerQuarter && isLastTab"
      class="alert alert-primary myuw-text-md"
      role="alert"
    >
      Most Summer quarter final examinations are given on the final meeting
      day of the course instead of a final examination week. Consult with
      your instructors when your final examinations will be.
    </div>
    <div v-if="hasMeetingsWithTime" class="mb-4 d-flex">
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
                  :is-finals-card="isFinalsTab" :day="day" :term="term"
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
              title="Select the Day of Week:"
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
                :key="j" :meeting-data="meetingData" :term="term"
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
        :meeting-data="{section: eosSection}" :term="term"
        :is-finals-card="false" class="d-inline-block w-auto mr-2"
      >
        <ol class="m-0 px-4 text-left">
          <li v-for="(meeting, j) in eosSection.meetings" :key="j">
            <span v-if="meeting.eos_start_date">
              {{ formatDate(meeting.eos_start_date) }}
              <span v-if="!meeting.start_end_same">
                &ndash; {{ formatDate(meeting.eos_end_date) }}
              </span>
            </span>
            <span v-if="meeting.wont_meet">
              Class does not meet
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
           style="min-width:110px;"
      >
        <uw-course-section :meeting-data="meeting" :term="term" />
      </div>
    </div>
  </div>
</template>

<script>
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
    term: {
      type: Object,
      required: true,
    },
    isLastTab: {  // MUWM-4987
      type: Boolean,
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
    quarterLastDate() {
      return this.term.last_day_instruction;
    },
    isSummerQuarter() {
      return this.term.quarter === 'summer';
    },
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
        this.period.earliestMeetingTime = this.nowDatetime()
            .clone().day(1).hour(8).minute(30);
        this.period.latestMeetingTime = this.nowDatetime()
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
            console.log(section.final_exam.start_date.format('dddd'));
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
        let addOnce = false;
        section.meetings.forEach((meeting) => {
          if (meeting.eos_start_date === null ||
              meeting.eos_end_date === null ||
              (meeting.eos_start_date >= this.period.start_date &&
               meeting.eos_start_date <= this.period.end_date ||
               meeting.eos_end_date >= this.period.start_date &&
               meeting.eos_end_date <= this.period.end_date
              )) {
            if (meeting.no_meeting ||
                meeting.start_time === null ||
                meeting.end_time === null) {
              if (!addOnce) {
                this.meetingsWithoutTime.push({
                  section: section,
                  meeting: meeting,
                  });
                addOnce = true;
                // add the same section only once
              }
            }
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
        renderTime: null,
      }];

      // Get time slot in 30 minutes interval
      if (startTime.minute() > 30) {
        startTime = startTime.add(30 - startTime.minute(), 'minutes');
      } else if (startTime.minute() < 30 && startTime.minute() !== 0) {
        startTime = startTime.subtract(startTime.minute(), 'minutes');
      }
      meetingsToAdd[0].renderTime = startTime;

      if (
        this.meetingMap[day][this.formatToUnique(startTime)] &&
        this.meetingMap[day][this.formatToUnique(startTime)].length > 0
      ) {
        meetingsToAdd = meetingsToAdd.concat(
            this.meetingMap[day][this.formatToUnique(startTime)],
        );
      }
      // MUWM-5001: course meets M-F, finals on Saturday
      // this.meetingMap[day] not initialized
      if (!this.meetingMap[day]) this.meetingMap[day] = {};
      this.meetingMap[day][this.formatToUnique(startTime)] = meetingsToAdd;
    },
    isDayDisabled(day) {
      return this.period.disabled_days && this.period.disabled_days[day];
    },
    // -- Some helper functions to initalize the state. --
    // Make a array of all the possible time slots with the interval
    // of this.timestep
    initializeTimeSlots() {
      // Generate start time
      let start = this.period.earliestMeetingTime.clone();
      if (start.minute() === 0) {
        start = start.subtract(1, 'hours');
      } else if (start.minute() > 30) {
        start = start.add(30 - start.minute(), 'minutes');
      } else {
        start = start.subtract(start.minute(), 'minutes');
      }

      // Generate end time
      let end = this.period.latestMeetingTime.clone();
      if (end.minute() === 0) {
        end = end.add(30, 'minutes');
      } else if (end.minute() > 30) {
        end = end.add(60 - end.minute(), 'minutes');
      } else {
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
        const dayToday = this.nowDatetime().format('dddd').toLowerCase();
        if (dayToday in this.period.daySlots) {
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
@use 'sass:math';
@import "../../../../css/myuw/variables.scss";

$heading-height: 45px;
$cell-height: 35px;

.time-column {
  padding-top: $heading-height - math.div($cell-height, 2);
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
