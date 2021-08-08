<template>
  <div v-if="collapsable" :id="collapseId"
    class="collapse"
  >
    <slot name="collapsible" />
  </div>
  <div v-else>
    <slot name="collapsible" />
  </div>
</template>

<script>
export default {
  props: {
    collapsable: {
      type: Boolean,
      default: true,
    },
    collapseId: {
      type: String,
      required: true,
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
