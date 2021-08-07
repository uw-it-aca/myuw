<template>
  <div :id="collapseId"
    class="collapse"
  >
    <slot name="collapsed" />
  </div>
</template>

<script>
export default {
  props: {
    collapseId: {
      type: String,
      required: true,
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
