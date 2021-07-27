<template>
  <div>
    <div v-b-toggle="collapseId">
      <slot name="heading">
      </slot>
    </div>
    <div :id="collapseId" class="collapse">
      <slot name="body">
      </slot>
    </div>
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