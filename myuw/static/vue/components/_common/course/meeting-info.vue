<template>
  <div>
    <div v-if="section.summer_term" class="d-flex">
      <h5
        :class="[!showRowHeading ? 'sr-only' : '']"
        class="w-25 font-weight-bold myuw-text-md"
      >
        Term
      </h5>
      <div class="flex-fill myuw-text-md">
        Summer
        {{
          section.summer_term
            .split('-')
            .map(ucfirst)
            .join('-')
        }}
      </div>
    </div>

    <div v-if="section.cc_display_dates" class="d-flex">
      <h5
        :class="[!showRowHeading ? 'sr-only' : '']"
        class="w-25 font-weight-bold myuw-text-md"
      >
        Dates
      </h5>
      <div class="flex-fill myuw-text-md">
        {{ sectionFormattedDates(section) }}
      </div>
    </div>

    <div v-if="section.on_standby" class="d-flex">
      <h5
        :class="[!showRowHeading ? 'sr-only' : '']"
        class="w-25 font-weight-bold myuw-text-md"
      >
        Your Status
      </h5>
      <div class="flex-fill myuw-text-md">
        On Standby
      </div>
    </div>

    <div class="d-flex">
      <h5
        :class="[!showRowHeading ? 'sr-only' : '']"
        class="w-25 font-weight-bold myuw-text-md"
      >
        Meeting Time
      </h5>
      <div class="flex-fill">
        <table class="mb-0 w-100 table table-sm table-borderless myuw-text-md">
          <thead class="sr-only">
            <tr>
              <th v-if="section.hasEosDates" :id="`dates-${section.id}`">
                Meeting Date(s)
              </th>
              <th :id="`days-${section.id}`">
                Meeting Day(s)
              </th>
              <th :id="`time-${section.id}`">
                Meeting Time
              </th>
              <th :id="`location-${section.id}`">
                Meeting Location
              </th>
              <th v-if="section.showMtgType" :id="`type-${section.id}`">
                Meeting Type
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(meeting, i) in section.meetings" :key="i">
              <td
                v-if="meeting.eos_start_date && meeting.eos_end_date"
                :headers="`dates-${meeting.id}`"
                class="p-0"
              >
                {{ formatEos(meeting) }}
              </td>
              <td
                v-if="meeting.wont_meet"
                colspan="3"
                :headers="`days-${meeting.id}`"
                p-0
              >
                <span class="text-muted">Class does not meet</span>
              </td>
              <td
                v-else-if="meeting.days_tbd"
                colspan="3"
                :headers="`days-${meeting.id}`"
                class="p-0"
              >
                <span class="text-muted">Days and times to be arranged</span>
              </td>
              <td
                v-else-if="meeting.no_meeting"
                colspan="3"
                :headers="`days-${meeting.id}`"
                class="p-0"
              >
                <span class="text-muted">
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
                <td
                  :headers="`time-${meeting.id}`"
                  class="p-0 text-center text-nowrap"
                >
                  {{ meeting.start_time.format('h:mm A') }} &ndash;
                  {{ meeting.end_time.format('h:mm A') }}
                </td>
                <td :headers="`location-${meeting.id}`" class="p-0 text-right">
                  <span v-if="meeting.is_remote">
                    Remote
                  </span>
                  <span v-else-if="meeting.building_tbd" class="text-muted">
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
              <td
                v-if="section.showMtgType"
                :headers="`type-${meeting.id}`"
                class="p-0"
              >
                <span v-if="meeting.displayType" :title="`${meeting.type}`">
                  {{ shortenMtgType(meeting.type) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
        <hr v-if="showRowHeading">
      </div>
    </div>
  </div>
</template>

<script>
import dayjs from 'dayjs';
export default {
  props: {
    section: {
      type: Object,
      required: true,
    },
    showRowHeading: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    sectionFormattedDates(section) {
      return `${dayjs(section.start_date).format('MMM D')} - ${dayjs(
          section.end_date).format('MMM D')}`;
    },
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
    shortenMtgType(typeStr) {
      if (typeStr.length > 4) {
        return typeStr.substring(0, 3).toUpperCase();
      }
      return typeStr.toUpperCase();
    },
  },
};
</script>
