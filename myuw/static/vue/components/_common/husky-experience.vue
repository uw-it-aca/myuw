<template>
  <uw-card v-if="hxtViewer" :loaded="isReady" :errored="isErrored" :errored-show="showError">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Husky Experience Toolkit
      </h2>
    </template>
    <template #card-body>
      <div class="mx-n3 mb-n3 myuw-huskyexp">
        <div class="position-relative overflow-hidden" style="max-height:300px;">
          <img :srcset="srcset" :src="src" class="img-fluid" :alt="alt" />
          <div class="position-absolute h-100 w-100 myuw-huskyexp-body">
            <a
              v-inner="articleTeaserTitle"
              :title="`${articleTeaserTitle}. ${articleTeaserBody}`"
              :href="expLink"
              class="d-block h-100 px-3 py-4"
            >
              <h3 class="myuw-teaser-title">
                <span class="bg-white h5 myuw-font-encode-sans px-2 py-1">{{
                  articleTeaserTitle
                }}</span>
              </h3>
              <span class="myuw-highlight text-body myuw-text-md">
                {{ articleTeaserBody }}
                <font-awesome-icon
                  v-if="articleFaClass"
                  :icon="articleFaClass"
                  aria-hidden="true"
                  class="align-text-bottom"
                />
              </span>
            </a>
          </div>
        </div>
      </div>
    </template>
  </uw-card>
</template>

<script>
import { faCaretRight } from '@fortawesome/free-solid-svg-icons';
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../_templates/card.vue';

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
      expLink: function(state) {
        return state.hx_toolkit.value[this.urlExtra].expLink;
      },
      srcset: function(state) {
        return state.hx_toolkit.value[this.urlExtra].srcset;
      },
      src: function(state) {
        return state.hx_toolkit.value[this.urlExtra].src;
      },
      alt: function(state) {
        return state.hx_toolkit.value[this.urlExtra].alt;
      },
      articleTeaserTitle: function(state) {
        return state.hx_toolkit.value[this.urlExtra].articleTeaserTitle;
      },
      articleTeaserBody: function(state) {
        return state.hx_toolkit.value[this.urlExtra].articleTeaserBody;
      },
      articleFaClass: function(state) {
        if (state.hx_toolkit.value[this.urlExtra].articleFaClass === 'caret-right') {
          return faCaretRight;
        }
        return null;
      },
      hxtViewer: state => state.user.affiliations.hxt_viewer,
    }),
    ...mapGetters('hx_toolkit', ['isReadyTagged', 'isErroredTagged', 'statusCodeTagged']),
    isReady() {
      return this.isReadyTagged(this.urlExtra);
    },
    isErrored() {
      return this.isErroredTagged(this.urlExtra);
    },
    statusCode() {
      return this.statusCodeTagged(this.urlExtra);
    },
    showError: function() {
      return this.isErrored && this.statusCode !== 404;
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
@import '../../../css/myuw/variables.scss';

.myuw-huskyexp {
  a {
    &:hover {
      text-decoration: none !important;
      h4 {
        color: $link-color !important;
        text-decoration: underline !important;
      }
      div {
        text-decoration: none !important;
      }
    }
  }
  img {
    opacity: 0.75;
  }
  .myuw-huskyexp-body {
    top: 0;
    padding: 2px;
  }

  .myuw-teaser-title {
    color: black;
    &:hover {
      color: $link-color !important;
      text-decoration: underline;
    }
  }

  .myuw-highlight {
    position: relative;
    left: 8px;
    padding: 3px 0;
    background: #ffffff;
    box-shadow: 8px 0 0 #ffffff, -8px 0 0 #ffffff;
    -webkit-box-decoration-break: clone;
    box-decoration-break: clone;
  }
}
</style>
