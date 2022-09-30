<template>
  <span v-if="meeting.is_remote">
    Remote
  </span>
  <span v-else-if="meeting.building_tbd"
    class="text-muted"
    title="Room to be arranged">
    Room TBD
  </span>
  <span v-else>
    <span v-if="meeting.building">
      <a v-if="meeting.latitude"
        :href="locationUrl"
        :title="`Map of ${meeting.building_name}`"
      >{{ meeting.building }}</a>
      <span v-else title="No building information available">
        {{ meeting.building }}
      </span>
    </span>

    <span v-if="meeting.room">
      <a v-if="meeting.classroom_info_url"
        :href="meeting.classroom_info_url"
        title="View classroom information"
      >{{ meeting.room }}</a>
      <span v-else title="No classroom information available">
        {{ meeting.room }}
        <a v-if="showRoomInfo && !meeting.room_tbd && meeting.room !== '*'"
          v-out="'No classroom info'"
          href=""><font-awesome-icon :icon="faQuestionCircle" /></a>
      </span>
    </span>
  </span>
</template>

<script>
import { faQuestionCircle } from '@fortawesome/free-solid-svg-icons';
export default {
  props: {
    meeting: {
      type: Object,
      required: true,
    },
    showRoomInfo: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      faQuestionCircle,
    };
  },
  computed: {
    locationUrl() {
      return `http://maps.google.com/maps?q=${this.meeting.latitude},${
        this.meeting.longitude
        }+(${this.encodeForMaps(this.meeting.building)})&z=18`;
    },
  },
};
</script>
