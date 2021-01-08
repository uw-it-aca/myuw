<template>
  <div>
    <div v-b-toggle="collapseId">
      <slot name="heading">
      </slot>
    </div>
    <b-collapse :id="collapseId">
      <slot name="body">
      </slot>
    </b-collapse>
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