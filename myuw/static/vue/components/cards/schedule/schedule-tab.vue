<template>
  <b-tab :title="title" title-item-class="text-uppercase" :active="active">
    <table v-if="hasMeetingsWithTime">
      <tr>
        <td />
        <th v-for="daySlot in daySlots" :key="daySlot" scope="col">
          {{days[daySlot]}}
        </th>
      </tr>
      <tr v-for="timeSlot in timeSlots" :key="timeSlot">
        <th scope="row"><div>{{timeSlot}}</div></th>
        <td v-for="({rowspan, day, meetings}, i) in meetingMap[timeSlot]"
            :key="i" :rowspan="rowspan"
            :class="{
              'bg-grey': 'disabled_days' in period && period.disabled_days[day]
            }"
        >
          <uw-course-mini-card v-if="meetings" :meetings="meetings"
                               :isFinalsCard="isFinalsTab"
          />
        </td>
      </tr>
    </table>
    <div v-if="meetingsWithoutTime.length > 0">
      <span v-if="!isFinalsTab">
        No meeting time specified:
      </span>
      <span v-else>
        Courses with final exam meeting times to be determined or courses with no final exam:
      </span>
      <div v-for="(meeting, i) in meetingsWithoutTime" :key="i">
        <uw-course-mini-card :meetings="[meeting]" />
      </div>
    </div>
  </b-tab>
</template>

<script>
import CourseMiniCard from './course-mini-card.vue';

export default {
  components: {
    'uw-course-mini-card': CourseMiniCard,
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
    }
  },
  data: function() {
    return {
      days: {
        monday: "MON",
        tuesday: "TUE",
        wednesday: "WED",
        thursday: "THU",
        friday: "FRI",
        saturday: "SAT",
        sunday: "SUN",
      },
      timestep: [30, 'minutes'],
      timeSlots: [],
      daySlots: [],
      meetingMap: {},
      meetingsWithoutTime: [],
      hasMeetingsWithTime: false,
      isFinalsTab: false,
    }
  },
  created() {
    // Set if this tab is for finals
    this.isFinalsTab = this.period.id == 'finals';

    // If there are no meetings with defined time in this period
    if (
      !(this.period.earliestMeetingTime == null &&
      this.period.latestMeetingTime == null)
    ) {
      // Make a array of all the possible time slots with the interval
      // of this.timestep
      let start = this.period.earliestMeetingTime.clone().subtract(
        ...this.timestep
      );
      let end = this.period.latestMeetingTime.clone().add(...this.timestep);
      if (!(end.minute() === 30 || end.minute() === 0)) {
        end = end.add(10, 'minutes');
      }

      while (start.format('hh:mm A') != end.format('hh:mm A')) {
        this.timeSlots.push(start.format('hh:mm A'));

        start = start.add(...this.timestep);
      }
      this.timeSlots.push(start.format('hh:mm A'));

      // Setting the days of the week that need to be displayed
      this.daySlots = ["monday", "tuesday", "wednesday", "thursday", "friday"];
      if (this.period.meets_saturday) {this.daySlots.push("saturday")};
      if (this.period.meets_sunday) {this.daySlots.unshift("sunday")};

      // Initalize the meeting map.
      for (const i in this.timeSlots) {
        this.meetingMap[this.timeSlots[i]] = {};
        for (const j in this.daySlots) {
          this.meetingMap[this.timeSlots[i]][this.daySlots[j]] = {
            rowspan: 1, day: this.daySlots[j],
          };
        }
      }

      // Put in the meeting with time into the map.
      for (const i in this.period.sections) {
        if (!this.isFinalsTab) {
          for (const j in this.period.sections[i].meetings) {
            if (this.period.sections[i].meetings[j].start_time && 
                this.period.sections[i].meetings[j].end_time) {
              for (const day in this.period.sections[i].meetings[j].meeting_days) {
                if (this.period.sections[i].meetings[j].meeting_days[day]) {
                  this.putMeeting(
                    this.period.sections[i],
                    this.period.sections[i].meetings[j],
                    this.period.sections[i].meetings[j].start_time,
                    this.period.sections[i].meetings[j].end_time,
                    day
                  );
                  this.hasMeetingsWithTime = true;
                }
              }
            }
          }
        } else {
          if (this.period.sections[i].final_exam &&
              this.period.sections[i].final_exam.start_date &&
              this.period.sections[i].final_exam.end_date) {
            this.putMeeting(
              this.period.sections[i],
              this.period.sections[i].final_exam,
              this.period.sections[i].final_exam.start_date,
              this.period.sections[i].final_exam.end_date,
              this.period.sections[i].final_exam.start_date.format(
                'dddd'
              ).toLowerCase()
            );
            this.hasMeetingsWithTime = true;
          }
        }
      }
    }

    // Put the meeting without time into its list.
    for (const i in this.period.sections) {
      if (!this.isFinalsTab) {
        for (const j in this.period.sections[i].meetings) {
          if (!(this.period.sections[i].meetings[j].start_time && 
              this.period.sections[i].meetings[j].end_time)) {
            this.meetingsWithoutTime.push({
              section: this.period.sections[i],
              meeting: this.period.sections[i].meetings[j],
            })
          }
        }
      } else {
        if (!(
            this.period.sections[i].final_exam &&
            this.period.sections[i].final_exam.start_date &&
            this.period.sections[i].final_exam.end_date)) {
          this.meetingsWithoutTime.push({
            section: this.period.sections[i],
            meeting: this.period.sections[i].final_exam,
          })
        }
      }
    }
  },
  methods: {
    putMeeting(section, meeting, startTime, endTime, day) {
      let meetingsToAdd = [{section: section, meeting: meeting}];

      let count = 1;
      const i = startTime.clone().add(...this.timestep);

      while (i < endTime) {
        // Check if this meeting is overwriting another
        if (
          this.meetingMap[i.format("hh:mm A")][day] &&
          this.meetingMap[i.format("hh:mm A")][day].meetings
        ) {
          meetingsToAdd = meetingsToAdd.concat(
            this.meetingMap[i.format("hh:mm A")][day].meetings
          );
        }
        delete this.meetingMap[i.format("hh:mm A")][day];
        i.add(...this.timestep);
        count += 1;
      }

      // Overlap handling when the starttime is diffrent
      if (!(day in this.meetingMap[startTime.format("hh:mm A")])) {
        // Find the overlapping meeting cell
        let newRowspan = count;
        const j = startTime.clone();
        while (!(day in this.meetingMap[j.format("hh:mm A")])) {
          j.subtract(...this.timestep);
          newRowspan += 1;
        }

        // Don't use the newRowspan in case of complete overlap
        if (this.meetingMap[j.format("hh:mm A")][day].rowspan < newRowspan) {
          this.meetingMap[j.format("hh:mm A")][day].rowspan = newRowspan;
        }

        this.meetingMap[j.format("hh:mm A")][day].meetings =
          this.meetingMap[j.format("hh:mm A")][day].meetings.concat(
          ...meetingsToAdd
        );
      } else {
        // Handle if the start time overlaps
        if (
          this.meetingMap[startTime.format("hh:mm A")][day].meetings &&
          this.meetingMap[startTime.format("hh:mm A")][day].meetings.length > 0
        ) {
          meetingsToAdd = meetingsToAdd.concat(
            this.meetingMap[startTime.format("hh:mm A")][day].meetings
          );
          // Select the bigger span
          if (
            this.meetingMap[startTime.format("hh:mm A")][day].rowspan > count
          ) {
            count = this.meetingMap[startTime.format("hh:mm A")][day].rowspan;
          }
        }

        // Update cell with the meeting
        this.meetingMap[startTime.format("hh:mm A")][day].rowspan = count;
        this.meetingMap[
          startTime.format("hh:mm A")
        ][day].meetings = meetingsToAdd;
      }
    }
  },
}
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