<template>
  <div v-if="estRegData.estRegDate" class="mb-4">
    <b-alert
      v-if="estRegData.isMy1stRegDay"
      show
      variant="primary"
      class="myuw-text-md"
    >
      Registration opens at 6:00AM
    </b-alert>

    <div v-else class="d-flex align-items-center">
      <h4 class="h6 m-0 text-dark font-weight-bold flex-fill">
        Est. Registration Date
      </h4>
      <div class="flex-fill text-right">
        <div class="font-weight-bold">
          {{ estRegData.estRegDate.date.format('ddd, MMM D') }}
        </div>
        <span class="myuw-text-md" aria-hidden="true">
          at 6:00 AM
        </span>
      </div>
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
