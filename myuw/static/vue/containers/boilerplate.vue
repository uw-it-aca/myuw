<template>
  <div>
    <myuw-header :disable_actions="disable_actions" :logout_url="logout_url" />

    <div id="content" role="main">
      <slot></slot>
    </div>

    <myuw-footer />
  </div>
</template>

<script>
import MyUWHeader from '../components/header.vue';
import MyUWFooter from '../components/footer.vue';

export default {
  components: {
    'myuw-header': MyUWHeader,
    'myuw-footer': MyUWFooter,
  },
  props: {
    disable_actions: Boolean,
    logout_url: String,
  },
  data: function () {
    return {};
  },
};
</script>

<style scoped>


</style>

<style>

</style>
