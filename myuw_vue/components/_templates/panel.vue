<template>
  <div v-if="loaded" :class="[$mq === 'mobile' ? 'px-3' : 'px-0']">
    <slot name="panel-body" />
  </div>
  <div v-else-if="errored" :class="[$mq === 'mobile' ? 'px-3' : 'px-0']">
    <slot name="panel-error" />
  </div>
  <div v-else>
    <div class="p-3 d-flex justify-content-center">
      <div class="spinner-border spinner-border-sm text-muted my-auto" role="status">
        <span class="visually-hidden">Loading...</span>
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
    errored: {
      type: Boolean,
      default: false,
    },
  },
  data: function() {
    return {};
  },
};
</script>
