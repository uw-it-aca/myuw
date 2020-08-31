<template>
  <b-tab :title="title" title-item-class="text-uppercase" :active="active">
    <table v-if="hasMeetingsWithTime">
      <tr>
        <td />
        <th v-for="daySlot in daySlots" :key="daySlot" scope="col"
            :aria-label="daySlot"
        >
          {{ days[daySlot] }}
          <br />
          <span v-if="isFinalsTab">
            {{getFirstFinalExamTimeOn(daySlot).format("MMM D")}}
          </span>
        </th>
      </tr>
      <tr v-for="timeSlot in timeSlots" :key="timeSlot">
        <th scope="row">
          <div>{{ timeSlot }}</div>
        </th>
        <td v-for="({rowspan, day, meetings}, i) in meetingMap[timeSlot]"
            :key="i" :rowspan="rowspan"
            :class="{
              'bg-grey': 'disabled_days' in period && period.disabled_days[day]
            }"
        >
          <uw-course-section v-if="meetings" :meetings="meetings"
                             :is-finals-card="isFinalsTab"
          />
        </td>
      </tr>
    </table>
    <div v-if="meetingsWithoutTime.length > 0">
      <span v-if="!isFinalsTab">
        No meeting time specified:
      </span>
      <span v-else>
        Courses with final exam meeting times to be determined or
        courses with no final exam:
      </span>
      <div v-for="(meeting, i) in meetingsWithoutTime" :key="i">
        <uw-course-section :meetings="[meeting]" />
      </div>
    </div>
  </b-tab>
</template>

<script>
import CourseSection from './course-section.vue';

export default {
  components: {
    'uw-course-section': CourseSection,
  },
  props: {
    title: {
      type: String,
      required: true,
    },
    active: {
      type: Boolean,
      default: false,
    },
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
    };
  },
  created() {
    // Set if this tab is for finals
    this.isFinalsTab = this.period.id == 'finals';

    // If there are no meetings with defined time in this period
    if (
      !(this.period.earliestMeetingTime == null &&
      this.period.latestMeetingTime == null)
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
                      section, meeting, meeting.start_time, meeting.end_time,
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
                section, section.final_exam, section.final_exam.start_date,
                section.final_exam.end_date,
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
        if (!(
          section.final_exam &&
          section.final_exam.start_date &&
          section.final_exam.end_date
        )) {
          this.meetingsWithoutTime.push({
            section: section,
            meeting: section.final_exam,
          });
        }
      }
    });
  },
  methods: {
    // Converts a moment object to a standard string that is used in timeslots
    toTimeSlotFormat(t) {
      return t.format('hh:mm A');
    },
    // Gets the meeting at the time t
    getMeetingsAt(t) {
      return this.meetingMap[this.toTimeSlotFormat(t)];
    },
    // Puts a meeting in meetingMap at time startTime and calculates variables
    // needed to render the meetingMap.
    putMeeting(section, meeting, startTime, endTime, day) {
      let meetingsToAdd = [{section: section, meeting: meeting}];

      let count = 1;
      const i = startTime.clone().add(...this.timestep);

      while (i < endTime) {
        // Check if this meeting is overwriting another
        if (
          this.getMeetingsAt(i)[day] &&
          this.getMeetingsAt(i)[day].meetings
        ) {
          meetingsToAdd = meetingsToAdd.concat(
              this.getMeetingsAt(i)[day].meetings,
          );
        }
        delete this.getMeetingsAt(i)[day];
        i.add(...this.timestep);
        count += 1;
      }

      // Overlap handling when the starttime is diffrent
      if (!(day in this.getMeetingsAt(startTime))) {
        // Find the overlapping meeting cell
        let newRowspan = count;
        const j = startTime.clone();
        while (!(day in this.getMeetingsAt(j))) {
          j.subtract(...this.timestep);
          newRowspan += 1;
        }

        // Don't use the newRowspan in case of complete overlap
        if (this.getMeetingsAt(j)[day].rowspan < newRowspan) {
          this.getMeetingsAt(j)[day].rowspan = newRowspan;
        }

        this.getMeetingsAt(j)[day].meetings =
          this.getMeetingsAt(j)[day].meetings.concat(
              ...meetingsToAdd,
          );
      } else {
        // Handle if the start time overlaps
        if (
          this.getMeetingsAt(startTime)[day].meetings &&
          this.getMeetingsAt(startTime)[day].meetings.length > 0
        ) {
          meetingsToAdd = meetingsToAdd.concat(
              this.getMeetingsAt(startTime)[day].meetings,
          );
          // Select the bigger span
          if (
            this.getMeetingsAt(startTime)[day].rowspan > count
          ) {
            count = this.getMeetingsAt(startTime)[day].rowspan;
          }
        }

        // Update cell with the meeting
        this.getMeetingsAt(startTime)[day].rowspan = count;
        this.getMeetingsAt(startTime)[day].meetings = meetingsToAdd;
      }
    },
    getFirstFinalExamTimeOn(day) {
      return this.period.latestMeetingTime.day(
        day.replace(/^([a-z])/, (c) => c.toUpperCase()),
      );
    },
    // -- Some helper functions to initalize the state. --
    // Make a array of all the possible time slots with the interval
    // of this.timestep
    initializeTimeSlots() {
      let start = this.period.earliestMeetingTime.clone().subtract(
          ...this.timestep,
      );
      let end = this.period.latestMeetingTime.clone().add(...this.timestep);
      if (!(end.minute() === 30 || end.minute() === 0)) {
        end = end.add(10, 'minutes');
      }

      while (this.toTimeSlotFormat(start) != this.toTimeSlotFormat(end)) {
        this.timeSlots.push(this.toTimeSlotFormat(start));

        start = start.add(...this.timestep);
      }
      this.timeSlots.push(this.toTimeSlotFormat(start));
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
    // Initalize the meeting map.
    initializeMeetingMap() {
      this.timeSlots.forEach((timeSlot) => {
        this.meetingMap[timeSlot] = {};
        this.daySlots.forEach((daySlot) => {
          this.meetingMap[timeSlot][daySlot] = {
            rowspan: 1, day: daySlot,
          };
        });
      });
    },
  },
};
</script>

<style lang="scss" scoped>
table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}
table, th, td {
  border: 1px solid black;
}
table > tr > td, th {
  position: relative;
}
table > tr > th > div {
  position: relative;
  bottom: 100%;
}
table > tr > td > div {
  position: absolute;
  top: 0;
}
</style>
