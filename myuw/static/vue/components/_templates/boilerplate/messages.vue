<template>
  <div
    v-if="displayOnboardMessage || bannerMessages.length > 0"
    class="w-100 myuw-messages bg-teal" role="complementary"
  >
    <div class="text-center text-white myuw-text-md">
      <h2 class="sr-only">
        Announcements
      </h2>
      <template v-if="bannerMessages.length > 0" id="message_banner_location">
        <div v-for="(message, i) in bannerMessages" id="messages" :key="i"
             class="message px-3 py-2"
        >
          {{ message }}
        </div>
      </template>
      <div v-if="displayOnboardMessage" class="px-3 py-2">
        New here?
        <b-link v-b-modal.tourModal class="text-white">
          <u>See MyUW at a glance</u>
        </b-link>
        <button type="button" aria-label="Close"
          class="close text-white"
          @click="hideOnboardMessage"><span aria-hidden="true">×</span></button>
      </div>
    </div>
  </div>
</template>

<script>
import {mapState, mapMutations} from 'vuex';
import axios from 'axios';
export default {
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
        this.addVarToState({
          name: 'displayOnboardMessage',
          value: false,
        });
      });
    },
    ...mapMutations([
      'addVarToState',
    ]),
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import "../../../../css/myuw/variables.scss";

//.myuw-messages {}

</style>
