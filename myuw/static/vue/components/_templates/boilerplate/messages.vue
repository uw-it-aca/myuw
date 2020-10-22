<template>
  <div class="myuw-messages bg-teal">
    <div class="px-3 py-2 text-center text-white myuw-text-md">
      <div>
        custom messages go here
      </div>
      <div>
        New here?
        <b-link v-b-modal.tourModal class="text-white-50">
          See MyUW at a glance
        </b-link>
        <!-- TODO: wire close button -->
        <b-button-close text-variant="light" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: function() {
    return {};
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import "../../../../css/myuw/variables.scss";

.myuw-messages {
  background: $gray-300;
}
</style>
