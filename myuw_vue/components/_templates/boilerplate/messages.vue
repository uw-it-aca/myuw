<template>
  <div
    v-if="showContent"
    class="w-100 myuw-messages" role="complementary"
  >
    <div class="text-center text-white myuw-text-md">
      <h2 class="visually-hidden">
        Announcements
      </h2>
      <template v-if="bannerMessages.length || hasPersMsgToDisplay"
        id="message_banner_location"
      >
        <uw-banner-message v-if="hasPersMsgToDisplay" :messages="persMessages" />

        <div v-for="(message, i) in bannerMessages" id="messages" :key="i"
          class="message px-3 py-2"
          v-html="message"
        ></div>
      </template>
      <div v-if="displayOnboardMessage" class="px-3 py-2 msg-onboard">
        New here?
        <a v-uw-modal.tourModal class="text-white"><u>See MyUW at a glance</u></a>
        <button
          type="button"
          class="btn-close btn-close-white align-top float-end"
          aria-label="Close"
          @click="hideOnboardMessage"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations} from 'vuex';
import axios from 'axios';
import BnrMessage from './banner_message.vue';
export default {
  components: {
    'uw-banner-message': BnrMessage,
  },
  computed: {
    ...mapState({
      bannerMessages: (state) => state.bannerMessages,
      persMessages: (state) => state.persMessages,
      displayOnboardMessage: (state) => state.displayOnboardMessage,
    }),
    hasPersMsgToDisplay() {
      return this.persMessages.length > 0;
    },
    showContent() {
      return (this.displayOnboardMessage || this.bannerMessages.length > 0 ||
        this.hasPersMsgToDisplay);
    },
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
@import '../../../../myuw/static/css/myuw/variables.scss';

.msg-onboard {  
  background-color: map.get($theme-colors, 'dark-beige');
}

</style>
