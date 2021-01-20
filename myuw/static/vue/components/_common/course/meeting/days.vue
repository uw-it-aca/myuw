<template>
  <span>
    <abbr v-if="meeting.meeting_days.monday" title="Monday">M</abbr>
    <abbr v-if="meeting.meeting_days.tuesday" title="Tuesday">T</abbr>
    <abbr v-if="meeting.meeting_days.wednesday" title="Wednesday">W</abbr>
    <abbr v-if="meeting.meeting_days.thursday" title="Thursday">Th</abbr>
    <abbr v-if="meeting.meeting_days.friday" title="Friday">F</abbr>
    <abbr v-if="meeting.meeting_days.saturday" title="Saturday">Sa</abbr>
    <abbr v-if="meeting.meeting_days.sunday" title="Sunday">Su</abbr>
  </span>
</template>
<script>
export default {
  props: {
    meeting: {
      type: Object,
      required: true,
    },
  },
};
</script>
