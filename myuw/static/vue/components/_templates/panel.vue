<template>
  <div v-if="(mobileOnly && $mq === 'mobile') || !mobileOnly">
    <div v-if="loaded" class="">
      <slot name="panel-body" />
    </div>
    <div v-else>
      <div class="p-3 d-flex justify-content-center">
        <b-spinner small variant="muted" class="my-auto" label="Loading..." />
      </div>
    </div>
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
