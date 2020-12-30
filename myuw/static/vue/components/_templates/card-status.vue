<template>
  <div class="mb-3">
    <div class="d-flex align-items-center">
      <h4 class="h6 m-0 text-dark font-weight-bold flex-fill">
        <slot name="status-label" />
      </h4>
      <div class="flex-fill text-right">
        <span class="h4 font-weight-bold">
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
