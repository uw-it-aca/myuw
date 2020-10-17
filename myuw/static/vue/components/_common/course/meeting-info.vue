<template>
  <b-col>
    <table class="w-100" style="table-layout: fixed;">
      <tr v-for="(meeting, i) in meetingsWithTime" :key="i">
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
        <td>
          {{ meeting.start_time }} &ndash; {{ meeting.end_time }}
        </td>
        <td>
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
        </td>
      </tr>
      <tr v-if="meetingsWithTime.length == 0">
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
    meetingsWithTime() {
      return this.meetings.filter((m) => m.start_time);
    },
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
  }
};
</script>

<style lang="scss" scoped>
tr {
  td:not(:first-child) {
    text-align: center;
  }
}
</style>
