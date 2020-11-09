<template>
  <div class="myuw-messages bg-teal" role="complimentary">
    <div class="px-3 py-2 text-center text-white myuw-text-md">
      <h2 class="sr-only">
        Announcements
      </h2>
      <div v-if="bannerMessages.length > 0" id="message_banner_location">
        <div v-for="(message, i) in bannerMessages" id="messages" :key="i">
          <div class="message">
            {{ message }}
          </div>
        </div>
      </div>
      <div v-if="!isHidden && displayOnboardMessage">
        New here?
        <b-link v-b-modal.tourModal class="text-white">
          <u>See MyUW at a glance</u>
        </b-link>
        <b-button-close text-variant="light" @click="hideOnboardMessage" />
      </div>
    </div>
  </div>
</template>

<script>
import {mapState} from 'vuex';
import axios from 'axios';
export default {
  data: function() {
    return {
      isHidden: false,
    };
  },
  computed: {
    ...mapState({
      bannerMessages: (state) => state.bannerMessages,
      displayOnboardMessage: (state) => state.displayOnboardMessage,
    }),
  },
  methods: {
    hideOnboardMessage: function(event) {
      axios.get('/api/v1/close_banner_message', {
        responseType: 'json',
      }).then((response) => {
        if (response.data.done) {
          this.isHidden = true;
        }
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import "../../../../css/myuw/variables.scss";

//.myuw-messages {}

</style>
