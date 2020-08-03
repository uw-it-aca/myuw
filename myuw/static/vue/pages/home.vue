<template>
  <div id="home">
    <small>home.vue (page component)</small>
    <div class="home">
      <hello-world class="sadf"></hello-world>
      <hello-world class="bal"></hello-world>
    </div>
  </div>
</template>

<script>
import HelloWorld from "../components/hello-world.vue";

export default {
  name: 'Home',
  components: {
    "hello-world": HelloWorld,
  }
};
</script>

<style lang="scss" scoped>
small { color: salmon; }
.home {
  outline: solid 2px salmon;
  padding: 10px;
  margin-bottom: 1.5rem;
}
</style>