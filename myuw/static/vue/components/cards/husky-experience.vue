<template>
  <uw-card v-if="hxtViewer" :loaded="isReady" :errored="isErrored">
    <template #card-heading>
      <h3 class="text-dark-beige">
        Husky Experience Toolkit
      </h3>
    </template>
    <template #card-body>
      <div class="mx-n3 overflow-hidden myuw-card-article"
           v-html="getArticleTeaserBody"
      />
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

<style lang="scss">
// scoped does not work... since the html content
// for the articles comes via the api
.myuw-card-article {
  border: solid 1px red; ;

  .myuw-card-image-full {
    width: 100%;
    height: auto;
    opacity: 0.75;
  }
}

</style>
