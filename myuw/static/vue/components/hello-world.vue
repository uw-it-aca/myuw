<template>
  <div class="hello card">
    <h3>{{ message }}</h3>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      message: 'Hello World',
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