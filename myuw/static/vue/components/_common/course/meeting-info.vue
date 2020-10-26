<template>
  <b-col>
    <table class="w-100" style="table-layout: fixed;">
      <thead class="sr-only">
        <tr>
            <th v-if="hasEosDates"
              :id="'dates-' + sectionId">Meeting Date(s)</th>
            <th :id="'days-' + sectionId">Meeting Day(s)</th>
            <th :id="'time-' + sectionId">Meeting Time</th>
            <th :id="'location-' + sectionId">Meeting Location</th>
            <th v-if="displayMeetingType" :id="'type-' + sectionId">
              Meeting Type</th>
        </tr>
    </thead>
    <tbody>
      <tr v-for="(meeting, i) in meetings" :key="i">
        <td v-if="meeting.eos_start_date && meeting.eos_end_date"
          :headers="'dates-' + meeting.id"
        >
          {{ formatEos(meeting) }}
        </td>
        <td v-if="meeting.wont_meet" colspan="3"
          :headers="'days-time-location-' + meeting.id"
        >
          Class does not meet
        </td>
        <td v-else-if="meeting.days_tbd" colspan="3"
          :headers="'days-time-location-' + meeting.id"
        >
          Days and times to be arranged
        </td>
        <td v-else-if="meeting.no_meeting" colspan="3"
          :headers="'days-time-location-' + meeting.id"
        >
          No classroom meeting: online learning
        </td>
        <template v-else-if="meeting.start_time && meeting.end_time">
          <td :headers="'days-' + meeting.id">
            <abbr v-if="meeting.meeting_days.monday" title="Monday">M</abbr>
            <abbr v-if="meeting.meeting_days.tuesday" title="Tuesday">T</abbr>
            <abbr v-if="meeting.meeting_days.wednesday" title="Wednesday">W
            </abbr>
            <abbr v-if="meeting.meeting_days.thursday" title="Thursday">Th
            </abbr>
            <abbr v-if="meeting.meeting_days.friday" title="Friday">F</abbr>
            <abbr v-if="meeting.meeting_days.saturday" title="Saturday">Sa
            </abbr>
            <abbr v-if="meeting.meeting_days.sunday" title="Sunday">Su</abbr>
          </td>
          <td :headers="'time-' + meeting.id">
            {{ meeting.start_time.format('h:mm A') }} &ndash;
            {{ meeting.end_time.format('h:mm A') }}
          </td>
          <td :headers="'location-' + meeting.id">
            <span v-if="meeting.is_remote">
              Remote
            </span>
            <span v-else-if="meeting.building_tbd">
              Room to be arranged
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
                title="View classroom information"
              >
                {{ meeting.room }}
              </a>
              <span
                v-else-if="meeting.room"
                title="No classroom information available"
              >
                {{ meeting.room }}
              </span>
            </span>
          </td>
        </template>
        <td v-if="displayMeetingType" :headers="'type-' + meeting.id">
          <span v-if="meeting.display_type">
            {{ meeting.type }}
          </span>
        </td>
      </tr>
    </tbody>
    </table>
  </b-col>
</template>

<script>
export default {
  props: {
    hasEosDates: {
      type: Boolean,
      required: true,
      default: false,
    },
    displayMeetingType: {
      type: Boolean,
      required: true,
      default: false,
    },
    meetings: {
      type: Array,
      required: true,
    },
    sectionId: {
      type: String,
      required: true,
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
    formatEos(meeting) {
      const startFormatted = meeting.eos_start_date.format('MMM D');
      const endFormatted = meeting.eos_end_date.format('MMM D');
      if (startFormatted == endFormatted) {
        return startFormatted;
      } else {
        return `${startFormatted} - ${endFormatted}`;
      }
    },
  },
};
</script>
