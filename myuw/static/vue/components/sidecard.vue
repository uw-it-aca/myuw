<template>
<div>
  <small>sidecard.vue (component)</small>
  <div class="side">
    <div class="card">
      <h3>{{ message }}</h3>
      <slot></slot>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'SideCard',
  data() {
    return {
      message: 'I am a sidecard',
    };
  },
};
</script>

<style lang="scss" scoped>

$coolColor: steelblue;

small { color: $coolColor; }
.side {
  outline: solid 2px $coolColor;
  padding: 10px;
  margin-bottom: 1.5rem;
}
</style>