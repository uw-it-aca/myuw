<template>
  <span v-if="isOnline">
    Online
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

      <span v-else>
        {{ meeting.room }}
        <span
          v-if="showRoomInfo && !meeting.room_tbd && meeting.room !== '*'"
          title="No classroom information available"
          class="text-dark-gray"
          aria-hidden="true"
        >
          <font-awesome-icon :icon="faInfoCircle" />
        </span>
      </span>
    </span>
  </span>
</template>

<script>
import { faInfoCircle } from '@fortawesome/free-solid-svg-icons';
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
      faInfoCircle,
    };
  },
  computed: {
    isOnline() {
      return (
        this.meeting.building_tbd &&
        (this.meeting.is_asynchronous ||
         this.meeting.is_synchronous ||
         this.meeting.is_hybrid) &&
        !(this.meeting.wont_meet ||
          this.meeting.no_meeting ||
          this.meeting.days_tbd)
      );
    },
    locationUrl() {
      return `http://maps.google.com/maps?q=${this.meeting.latitude},${
        this.meeting.longitude
        }+(${this.encodeForMaps(this.meeting.building)})&z=18`;
    },
  },
};
</script>
