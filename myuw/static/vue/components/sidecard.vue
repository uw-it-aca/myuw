<template>
  <div class="side card">
    <h3>{{ message }}</h3>
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      message: 'I am a sidecard',
    };
  },
};
</script>

<style lang="scss" scoped>

$coolColor: lime;

.hello {
  margin-bottom: 1.5rem;
}
</style>