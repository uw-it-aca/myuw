<template>
  <div class="myuw-messages bg-teal" role="complimentary">
    <div class="px-3 py-2 text-center text-white myuw-text-md">
      <h2 class="sr-only">
        Announcements
      </h2>
      <div id="message_banner_location">
        custom messages go here
      </div>
      <!-- {% if banner_messages %}
      <div id="message_banner_location">
        <div v-for="(message, i) in banner_messages" id="messages" :key="i"
             class="message-text myuw-wrapper"
        >
          <div class="message">
            <p>{{ message.message_body }}</p>
          </div>
        </div>
      </div> -->
      <!-- {% if display_onboard_message %} -->
      <div v-if="!isHidden">
        New here?
        <b-link v-b-modal.tourModal class="text-white">
          <u>See MyUW at a glance</u>
        </b-link>
        <b-button-close text-variant="light" @click="hideTourMessage" />
      </div>
    </div>
  </div>
</template>

<script>
import {mapState} from 'vuex';
export default {
  data: function() {
    return {
      isHidden: false,
    };
  },
  computed: {
    ...mapState({
      // banner_messages: (state) => state.
    }),
  },
  methods: {
    hideTourMessage: function(event) {
      // TODO: wire up with api
      this.isHidden = true;
      /*
      $.ajax({
            url: "/api/v1/close_banner_message",
            dataType: "JSON",
            async: true,
            type: 'GET',
            accepts: {html: "text/html"},
            success: function(results) {
                if (results.done) {
                    desktop_div.className += " hidden";
                    mobile_div.className += " hidden";
                }
            },
            error: function(xhr, status, error) {
                return false;
            }
        });
      */
    },
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import "../../../../css/myuw/variables.scss";

//.myuw-messages {}

</style>
