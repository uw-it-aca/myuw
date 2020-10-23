<template>
  <b-col>
    <table class="w-100" style="table-layout: fixed;">
      <tr v-for="(meeting, i) in meetingOnlyIfHasTime" :key="i">
        <td v-if="meeting.eos_start_date && meeting.eos_end_date">
          {{ formatEos(meeting) }}
        </td>
        <td>
          <abbr v-if="meeting.meeting_days.monday" title="Monday">M</abbr>
          <abbr v-if="meeting.meeting_days.tuesday" title="Tuesday">T</abbr>
          <abbr
            v-if="meeting.meeting_days.wednesday"
            title="Wednesday"
          >
            W
          </abbr>
          <abbr v-if="meeting.meeting_days.thursday" title="Thursday">Th</abbr>
          <abbr v-if="meeting.meeting_days.friday" title="Friday">F</abbr>
          <abbr v-if="meeting.meeting_days.saturday" title="Saturday">Sa</abbr>
          <abbr v-if="meeting.meeting_days.sunday" title="Sunday">Su</abbr>
        </td>
        <!-- Shares if conditional -->
        <td v-if="meeting.start_time && meeting.end_time">
          {{ meeting.start_time.format('h:mm A') }} &ndash;
          {{ meeting.end_time.format('h:mm A') }}
        </td>
        <!-- Shares if conditional -->
        <td v-if="meeting.start_time && meeting.end_time">
          <span v-if="meeting.is_remote">
            Remote
          </span>
          <span v-else>
            <a
              v-if="locationUrl(meeting)"
              :href="locationUrl(meeting)"
              target="_blank"
              :title="`Map ${meeting.building}`"
            >
              {{ meeting.building }}
            </a>
            <a
              v-if="meeting.classroom_info_url"
              :href="meeting.classroom_info_url"
              target="_blank"
            >
              {{ meeting.room }}
            </a>
            <span
              v-else-if="meeting.room"
              title="No classroom information available"
            >
              {{ meeting.room === '*' ? 'Room to be arranged' : meeting.room }}
            </span>
          </span>
        </td>
        <td v-else>
          Class does not meet
        </td>
      </tr>
      <tr v-if="meetingOnlyIfHasTime.length == 0">
        <td>
          Days and times to be arranged
        </td>
      </tr>
    </table>
  </b-col>
</template>

<script>
export default {
  props: {
    meetings: {
      type: Array,
      required: true,
    },
  },
  computed: {
    meetingOnlyIfHasTime() {
      if (this.meetings.find((m) => m.start_time)) {
        return this.meetings;
      }
      return [];
    }
  },
  methods: {
    locationUrl(meeting) {
      if (meeting.latitude) {
        return `http://maps.google.com/maps?q=${meeting.latitude},${
          meeting.longitude
        }+(${this.encodeForMaps(meeting.building_name)})&z=18`;
      }
      return null;
    },
    formatEos(meeting) {
      const startFormatted = meeting.eos_start_date.format('MMM D');
      const endFormatted = meeting.eos_end_date.format('MMM D');
      if (startFormatted == endFormatted) {
        return startFormatted;
      } else {
        return `${startFormatted} - ${endFormatted}`;
      }
    }
  },
};
</script>
