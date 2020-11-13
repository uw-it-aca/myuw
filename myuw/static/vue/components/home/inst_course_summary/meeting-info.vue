<template>
  <div>
    <table>
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
          <th :id="`enrollment-${section.id}`">
            Enrollment
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="meeting in section.meetings"
          :key="meeting.id"
        >
          <td
            v-if="meeting.eos_start_date && meeting.eos_end_date"
            :headers="`dates-${meeting.id}`"
          >
            {{ formatEos(meeting) }}
          </td>
          <td
            v-if="meeting.wont_meet"
            colspan="3"
            :headers="`days-${meeting.id}`"
            p-0
          >
            <span>Class does not meet</span>
          </td>
          <td
            v-else-if="meeting.days_tbd"
            colspan="3"
            :headers="`days-${meeting.id}`"
          >
            <span>Days and times to be arranged</span>
          </td>
          <td
            v-else-if="meeting.no_meeting"
            colspan="3"
            :headers="`days-${meeting.id}`"
          >
            <span>
              No classroom meeting: online learning
            </span>
          </td>
          <template v-else-if="meeting.start_time && meeting.end_time">
            <td :headers="`days-${meeting.id}`">
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
            >
              {{ meeting.start_time.format('h:mm A') }} &ndash;
              {{ meeting.end_time.format('h:mm A') }}
            </td>
            <td :headers="`location-${meeting.id}`">
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
          <td
            :headers="`enrollment-${meeting.id}`"
          >
            <div>
              <span v-if="section.is_prev_term_enrollment">
                0<!-- the current_enrollment value is of previous term -->
                <span v-if="!section.is_independent_study">
                  &nbsp;of&nbsp;{{ section.limit_estimate_enrollment }}
                </span>
              </span>

              <span v-else-if="!section.current_enrollment">
                0<span v-if="!section.is_independent_study">
                  &nbsp;of&nbsp;{{ section.limit_estimate_enrollment }}
                </span>
              </span>

              <span v-else>
                <a
                  target="_blank"
                  :href="classListHref(section)"
                  :rel="section.section_label"
                  title="View class list"
                >
                  {{ section.current_enrollment }}
                  <span v-if="!section.is_independent_study">
                    <span>&nbsp;of&nbsp;</span><span>/</span>
                    {{ section.limit_estimate_enrollment }}
                  </span>
                </a>
              </span>
            </div>
          </td>
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
    classListHref(section) {
      return ('/teaching/' + section.year + ',' +
              section.quarter + ',' + section.curriculum_abbr + ',' +
              section.course_number + '/' + section.section_id + '/students');
    },
  },
};
</script>
