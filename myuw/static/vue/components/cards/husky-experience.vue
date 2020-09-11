<template>
  <uw-card v-if="hxtViewer" :loaded="isReady" :errored="isErrored">
    <template #card-heading>
      <h3>
        Husky Experience Toolkit
      </h3>
    </template>
    <template #card-body>
      <div v-html="getArticleTeaserBody" />
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
    return {
      urlExtra: 'week/',
    };
  },
  computed: {
    ...mapState({
      hx_toolkit: (state) => state.hx_toolkit.value,
      hxtViewer: (state) => state.user.affiliations.hxt_viewer,
    }),
    ...mapGetters('hx_toolkit', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
    getArticleTeaserBody() {
      const parser = new DOMParser();
      const articleHtml = this.hx_toolkit[this.urlExtra];
      const htmlDoc = parser.parseFromString(
          articleHtml, 'text/html',
      );

      if (htmlDoc.links[0] !== undefined) {
        return htmlDoc.links[0].outerHTML;
      } else {
        return articleHtml;
      }
    },
  },
  created() {
    if (this.hxtViewer) {
      this.fetch(this.urlExtra);
    }
  },
  methods: {
    ...mapActions('hx_toolkit', ['fetch']),

  },
};
</script>

<style lang="scss" scoped>
</style>
