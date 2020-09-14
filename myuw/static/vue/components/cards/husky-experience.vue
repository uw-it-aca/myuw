<template>
  <uw-card v-if="hxtViewer" :loaded="isReady" :errored="isErrored">
    <template #card-heading>
      <h3 class="text-dark-beige">
        {{cardTitle}}
      </h3>
    </template>
    <template #card-body>
      <a :href="expLink">
        <img :srcset="srcset" :src="src"/>
        <div>
          <h4>{{articleTeaserTitle}}</h4>
          {{articleTeaserBody}}
          <font-awesome-icon :icon="['fas', articleFaClass]" />
        </div>
      </a>
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
      cardTitle: function(state) { 
        return state.hx_toolkit.value[this.urlExtra].cardTitle
      },
      expLink: function(state) { 
        return state.hx_toolkit.value[this.urlExtra].expLink
      },
      srcset: function(state) { 
        return state.hx_toolkit.value[this.urlExtra].srcset
      },
      src: function(state) { 
        return state.hx_toolkit.value[this.urlExtra].src
      },
      articleTeaserTitle: function(state) { 
        return state.hx_toolkit.value[this.urlExtra].articleTeaserTitle
      },
      articleTeaserBody: function(state) { 
        return state.hx_toolkit.value[this.urlExtra].articleTeaserBody
      },
      articleFaClass: function(state) { 
        return state.hx_toolkit.value[this.urlExtra].articleFaClass
      },
      hxtViewer: (state) => state.user.affiliations.hxt_viewer,
    }),
    ...mapGetters('hx_toolkit', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
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
