<template>
  <div class="mb-3">
    <div class="d-flex align-items-center">
      <h3 class="h6 m-0 myuw-font-encode-sans flex-fill">
        <slot name="status-label" />
      </h3>
      <div class="flex-fill text-right">
        <span class="h4 myuw-font-encode-sans">
          <slot name="status-value" />
        </span>
      </div>
    </div>
    <div>
      <slot name="status-content" />
    </div>
  </div>
</template>

<script>
export default {
  data: function () {
    return {};
  },
};
</script>
