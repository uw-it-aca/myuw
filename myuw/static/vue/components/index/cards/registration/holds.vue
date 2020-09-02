<template>
  <div>
    <h4 v-if="!myplanPeakLoad">Holds</h4>
    <div>
      <font-awesome-icon
        :icon="['fas', 'exclamation-triangle']"
        class="mr-1"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    myplanPeakLoad: {
      type: Boolean,
      required: true,
    },
    summerCardLabel: {
      type: String,
      default: null,
    },
    regHoldsNotices: {
      type: Array,
      required: true,
    }
  },
}
</script>

<style lang="scss" scoped>

</style>