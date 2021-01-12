<template>
  <div>
    <table class="mb-0 table table-sm table-borderless myuw-text-md">
      <thead class="sr-only">
        <tr>
          <th v-if="section.hasEosDates" :id="`dates-${section.id}`">
            Meeting Date(s)
          </th>
          <th :id="`days-${section.id}`">
            Day(s)
          </th>
          <th :id="`time-${section.id}`">
            Time
          </th>
          <th :id="`location-${section.id}`">
            Location
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="meeting in section.meetings" :key="meeting.id">
          <td v-if="meeting.eos_start_date && meeting.eos_end_date"
              :headers="`dates-${meeting.id}`"
          >
            {{ formatEos(meeting) }}
          </td>
          <td v-if="meeting.wont_meet" colspan="3"
              :headers="`days-${meeting.id}`" p-0
          >
            <span>Class does not meet</span>
          </td>
          <td v-else-if="meeting.days_tbd" colspan="3"
              :headers="`days-${meeting.id}`"
          >
            <span>Days and times to be arranged</span>
          </td>
          <td v-else-if="meeting.no_meeting" colspan="3"
              :headers="`days-${meeting.id}`"
          >
            <span>
              No classroom meeting: online learning
            </span>
          </td>
          <template v-else-if="meeting.start_time && meeting.end_time">
            <td :headers="`days-${meeting.id}`" class="p-0 text-nowrap">
              <abbr v-if="meeting.meeting_days.monday" title="Monday">
                M</abbr>
              <abbr v-if="meeting.meeting_days.tuesday" title="Tuesday">
                T</abbr>
              <abbr v-if="meeting.meeting_days.wednesday" title="Wednesday">
                W</abbr>
              <abbr v-if="meeting.meeting_days.thursday" title="Thursday">
                Th</abbr>
              <abbr v-if="meeting.meeting_days.friday" title="Friday">
                F</abbr>
              <abbr v-if="meeting.meeting_days.saturday" title="Saturday">
                Sa</abbr>
              <abbr v-if="meeting.meeting_days.sunday" title="Sunday">
                Su</abbr>
            </td>
            <td :headers="`time-${meeting.id}`" class="p-0 text-nowrap">
              {{ meeting.start_time.format('h:mm A') }} &ndash;
              {{ meeting.end_time.format('h:mm A') }}
            </td>
            <td :headers="`location-${meeting.id}`" class="p-0">
              <span v-if="meeting.is_remote">
                Remote
              </span>
              <span v-else-if="meeting.building_tbd">
                Room to be arranged
              </span>
              <span v-else>
                <span v-if="meeting.building">
                  <a v-if="meeting.latitude"
                    :href="locationUrl(meeting)"
                    target="_blank"
                    :title="`Map of ${meeting.building}`"
                  >{{ meeting.building }}</a>
                  <span v-else title="No building information available">
                    {{ meeting.building }}
                  </span>
                </span>

                <span v-if="meeting.room">
                  <a
                    v-if="meeting.classroom_info_url"
                    :href="meeting.classroom_info_url"
                    target="_blank"
                    title="View classroom information"
                  >{{ meeting.room }}</a>
                  <span v-else title="No classroom information available">
                    {{ meeting.room }}
                  </span>
                </span>
              </span>
            </td>
          </template>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
  methods: {
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
