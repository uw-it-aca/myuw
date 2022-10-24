<template>
  <div class="small text-center border border-danger mb-3 mx-auto">
    <span class="me-2 fst-italic text-muted" >{{ prompt }}</span
    >
    <a href="" class="text-nowrap">Share your feedback</a>

    <div>{{ formUrl }}</div>
  </div>
</template>

<script>

export default {
  props: {
    prompt: {
      type: String,
      required: true,
    },
    formUrl: {
      type: String,
      required: true,
    },
  },
  data: function() {
    return {};
  },

};
</script>
