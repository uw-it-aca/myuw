<template>
  <div v-if="estRegData.estRegDate" class="mb-4">
    <div v-if="estRegData.isMy1stRegDay"
         class="alert alert-primary" role="alert"
    >
      Registration opens at 6:00AM
    </div>
    <div v-else class="d-flex align-items-center">
      <h4 class="h6 m-0 text-dark font-weight-bold flex-fill"
          aria-label="Estimated Registration Date"
      >
        Est. Registration Date
      </h4>
      <div class="flex-fill text-right">
        <div
          class="font-weight-bold"
          :aria-label="`${
            estRegData.estRegDate.date.format('ddd, MMM D')
          } at 6:00 AM`"
        >
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
