<template>
  <div
    v-if="displayOnboardMessage || bannerMessages.length > 0"
    class="w-100 myuw-messages bg-teal"
    role="complementary"
  >
    <div class="text-center text-white myuw-text-md">
      <h2 class="visually-hidden">
        Announcements
      </h2>
      <template v-if="bannerMessages.length > 0" id="message_banner_location">
        <div
          v-for="(message, i) in bannerMessages"
          id="messages"
          :key="i"
          class="message px-3 py-2"
        >
          {{ message }}
        </div>
      </template>
      <div v-if="displayOnboardMessage" class="px-3 py-2">
        New here?

        <a role="button" class="text-white" data-toggle="modal" data-target="#tourModal">
          <u>See MyUW at a glance</u>
        </a>

        <button
          type="button"
          class="btn-close btn-close-white"
          aria-label="Close"
          @click="hideOnboardMessage"
        ></button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import axios from 'axios';
export default {
  computed: {
    ...mapState({
      bannerMessages: state => state.bannerMessages,
      displayOnboardMessage: state => state.displayOnboardMessage,
    }),
  },
  methods: {
    hideOnboardMessage: function(event) {
      axios
        .get('/api/v1/close_banner_message', {
          responseType: 'json',
        })
        .then(response => {
          this.addVarToState({
            name: 'displayOnboardMessage',
            value: false,
          });
        });
    },
    ...mapMutations(['addVarToState']),
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import '../../../../css/myuw/variables.scss';

//.myuw-messages {}
</style>
