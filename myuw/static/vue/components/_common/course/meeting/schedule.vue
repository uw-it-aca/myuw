<template>
<div class="d-flex">
    <h3 v-if="!noHeading"
      class="h6 text-dark-beige myuw-font-encode-sans"
      :class="[!showRowHeading ? 'sr-only' : '']"
    >
      Meeting Time
    </h3>
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
          <tr v-for="meeting in section.meetings" :key="meeting.id">
            <td v-if="section.hasEosDates"
              :headers="`dates-${meeting.id}`"
              class="p-0"
            >
              <span v-if="meeting.eos_start_date && meeting.eos_end_date">
                {{ formatEos(meeting) }}
              </span>
            </td>

            <td v-if="meeting.wont_meet"
              :headers="`days-${meeting.id}`"
              colspan="3" class="p-0"
            >
              <span class="text-muted">Class does not meet</span>
            </td>

            <td v-else-if="meeting.days_tbd"
              :headers="`days-${meeting.id}`"
              colspan="3" class="p-0"
            >
              <span class="text-muted">Days and times to be arranged</span>
            </td>

            <td v-else-if="meeting.no_meeting"
              :headers="`days-${meeting.id}`"
              colspan="3" class="p-0"
            >
              <span class="text-muted">No classroom meeting: online learning</span>
            </td>

            <template v-else-if="meeting.start_time && meeting.end_time">
              <td :headers="`days-${meeting.id}`"
                class="p-0 text-nowrap"
              >
                <uw-meeting-days :meeting="meeting" />
              </td>
              <td :headers="`time-${meeting.id}`"
                class="p-0 text-center text-nowrap"
              >
                {{ meeting.start_time.format('h:mm A') }} &ndash;
                {{ meeting.end_time.format('h:mm A') }}
              </td>
              <td :headers="`location-${meeting.id}`"
                class="p-0 text-right text-nowrap"
              >
                <uw-meeting-location :meeting="meeting" />
              </td>
            </template>

            <td v-if="section.showMtgType"
              :headers="`type-${meeting.id}`"
              class="p-0 text-right"
            >
              <span v-if="meeting.displayType" :title="`${meeting.type}`"
                    :class="`px-1 border myuw-text-sm
                    text-uppercase text-c${section.color_id}`"
              >
                {{ shortenMtgType(meeting.type) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    <hr v-if="showRowHeading">
    </div>
  </div>
</template>

<script>
import Days from './days.vue';
import Location from './location.vue';
export default {
  components: {
    'uw-meeting-days': Days,
    'uw-meeting-location': Location,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
    showRowHeading: {
      type: Boolean,
      default: false,
    },
    noHeading: {
      type: Boolean,
      default: false,
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
    shortenMtgType(typeStr) {
      if (typeStr.length > 4) {
        return typeStr.substring(0, 3).toUpperCase();
      }
      return typeStr.toUpperCase();
    },
  },
};
</script>
