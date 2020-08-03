<template>
  <div class="hello card">
    <h3>{{ message }}</h3>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
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