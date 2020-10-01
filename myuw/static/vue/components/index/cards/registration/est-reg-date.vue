<template>
  <div v-if="estRegData.estRegDate">
    <span class="sr-only">
      Estimated Registration Date: {{ estRegData.estRegDate.date }}
    </span>
    <h4>Est. Registration Date</h4>
    <div>
      <span>
        {{ estRegData.estRegDate.date.format('ddd, MMM D') }}
      </span>
      <br>
      <span>
        at 6:00 AM
      </span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    estRegData: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>

</style>
