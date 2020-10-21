<template>
  <div v-if="(mobileOnly && $mq === 'mobile') || !mobileOnly">
    <b-container v-if="loaded" class="">
      <slot name="panel-body" />
    </b-container>
    <b-container v-else>
      <div class="p-3 d-flex justify-content-center">
        <b-spinner small variant="muted" class="my-auto" label="Loading..." />
      </div>
    </b-container>
  </div>
</template>

<script>
export default {
  props: {
    loaded: {
      type: Boolean,
      default: false,
    },
    mobileOnly: {
      type: Boolean,
      default: false,
    },
  },
  data: function() {
    return {};
  },
};
</script>
