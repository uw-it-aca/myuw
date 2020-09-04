<template>
  <uw-card :loaded="isReady" :errored="isErrored">
    <template #card-heading>
      <h3>
        Husky Experience Toolkit
      </h3>
    </template>
    <template #card-body>
      <div v-html="article_html" />
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../containers/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  data: function() {
    return {};
  },
  computed: {
    ...mapState({
      article_html: (state) => state.hx_toolkit.value.article_html,

    }),
    ...mapGetters('hx_toolkit', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
  },
  created() {
    this.fetch();
  },
  methods: {
    ...mapActions('hx_toolkit', ['fetch']),
  },
};
</script>

<style lang="scss" scoped>
</style>
