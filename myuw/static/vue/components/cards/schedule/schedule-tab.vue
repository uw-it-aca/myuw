<template>
  <b-tab :title="title" title-item-class="text-uppercase" :active="active">
    <table>
      <tr>
        <td />
        <th v-for="daySlot in daySlots" :key="daySlot" scope="col">
          {{days[daySlot]}}
        </th>
      </tr>
      <tr v-for="timeSlot in timeSlots" :key="timeSlot">
        <th scope="row"><div>{{timeSlot}}</div></th>
        <td v-for="(daySlot, i) in meetingMap[timeSlot]" :key="i"
            :rowspan="daySlot.rowspan">
          {{daySlot.data ? daySlot.data.course_title + ' ' + daySlot.data.course_number : ''}}
        </td>
      </tr>
    </table>
  </b-tab>
</template>

<script>
export default {
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
        sunday: null,
      },
      timestep: [30, 'minutes'],
      timeSlots: [],
      daySlots: [],
      meetingMap: {},
    }
  },
  created() {
    let start = this.period.minMeetingTime.clone().subtract(
        ...this.timestep
      );
    let end = this.period.maxMeetingTime.clone().add(...this.timestep);
    if (!(end.minute() === 30 || end.minute() === 0)) {
      end = end.add(10, 'minutes');
    }

    while (start.format('hh:mm A') != end.format('hh:mm A')) {
      this.timeSlots.push(start.format('hh:mm A'));

      start = start.add(...this.timestep);
    }
    this.timeSlots.push(start.format('hh:mm A'));

    // Stud
    this.daySlots = ["monday", "tuesday", "wednesday", "thursday", "friday"];

    // Initalize the meeting map.
    for (const i in this.timeSlots) {
      this.meetingMap[this.timeSlots[i]] = {};
      for (const j in this.daySlots) {
        this.meetingMap[this.timeSlots[i]][this.daySlots[j]] = {
          rowspan: 1,
        };
      }
    }

    for (const i in this.period.sections) {
      if (this.period.id != 'finals') {
        for (const j in this.period.sections[i].meetings) {
          if (this.period.sections[i].meetings[j].start_time && 
              this.period.sections[i].meetings[j].end_time) {
            for (const day in this.period.sections[i].meetings[j].meeting_days) {
              if (this.period.sections[i].meetings[j].meeting_days[day]) {
                this.putMeeting(
                  this.period.sections[i],
                  this.period.sections[i].meetings[j].start_time,
                  this.period.sections[i].meetings[j].end_time,
                  day
                );
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
            this.period.sections[i].final_exam.start_date,
            this.period.sections[i].final_exam.end_date,
            this.period.sections[i].final_exam.start_date.format(
              'dddd'
            ).toLowerCase()
          );
        }
      }
    }
  },
  computed: {
  },
  methods: {
    putMeeting(section, startTime, endTime, day) {
      let count = 1;
      console.log(this.period.id, this.meetingMap["05:00 PM"]);
      console.log(this.period.id, section);
      const i = startTime.clone().add(...this.timestep);
      console.log('Proccessing', startTime.format("hh:mm A"), '-', endTime.format("hh:mm A"), day);
      while (i < endTime) {
        console.log("Deleting", i.format("hh:mm A"), day);
        delete this.meetingMap[i.format("hh:mm A")][day];
        i.add(...this.timestep);
        count += 1;
      }

      console.log(day);
      // Update the rowspan
      this.meetingMap[startTime.format("hh:mm A")][day].rowspan = count;
      this.meetingMap[startTime.format("hh:mm A")][day].data = section;
    }
  },
}
</script>

<style lang="scss" scoped>
table {
  border-collapse: collapse;
}
table, th, td {
  border: 1px solid black;
}
// table > tr > th > div {
//   position: relative;
//   top: 0.85rem;
// }
</style>