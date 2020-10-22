<template>
  <div class="myuw-messages bg-teal">
    <div class="px-3 py-2 text-center text-white myuw-text-md">
      <h2 class="sr-only">
        Announcements
      </h2>
      <div id="message_banner_location">
        custom messages go here
      </div>
      <div v-if="!isHidden">
        New here?
        <b-link v-b-modal.tourModal class="text-white">
          <u>See MyUW at a glance</u>
        </b-link>
        <!-- TODO: wire close button -->
        <b-button-close text-variant="light" @click="hideTourMessage" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      isHidden: false,
    };
  },
  methods: {
    hideTourMessage: function(event) {
      console.log('sadfasdf');
      this.isHidden = true;
    },
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import "../../../../css/myuw/variables.scss";

//.myuw-messages {}

</style>
