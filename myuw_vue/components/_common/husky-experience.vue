<template>
  <uw-card v-if="hxtViewer" :loaded="isReady" :errored="isErrored" :errored-show="showError">
    <template #card-heading>
      <template v-if="page.title == 'Home'">
        <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Husky Experience Toolkit</h2>
      </template>
      <template v-else>
        <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Featured Article</h2>
      </template>
    </template>
    <template #card-body>
      <div class="mb-2">
        <div class="myuw-text-md me-auto">
          <div class="row">
            <div class="col-10 col-lg-4">
              <img :srcset="srcset" :src="src" class="img-fluid border" :alt="alt" />
            </div>
            <div class="col-10 col-lg-6">
              <h3 class="myuw-teaser-title h6 myuw-font-encode-sans mb-1 mt-3 mt-lg-0">
                {{ articleTeaserTitle }}
              </h3>
              <div class="myuw-text-md mb-1">
                {{ articleTeaserBody }}
                <a
                  v-inner="articleTeaserTitle"
                  :title="`${articleTeaserTitle}. ${articleTeaserBody}`"
                  :href="expLink"
                >
                  Read more
                </a>
              </div>
              <div class="mb-3 text-secondary">
                <em>2 min read time</em>
              </div>
              <div v-if="page.title == 'Home'">
                <a class="myuw-text-md" href="https://my.uw.edu/husky_experience/"
                  >Learn more about the toolkit</a
                >
              </div>
            </div>
          </div>
          <div class="myuw-chevron">
            <a
              v-inner="articleTeaserTitle"
              :title="`${articleTeaserTitle}. ${articleTeaserBody}`"
              :href="expLink"
            >
              <span class="visually-hidden"> link to article </span>
              <font-awesome-icon :icon="faChevronRight" />
            </a>
          </div>
        </div>
      </div>
    </template>
  </uw-card>
</template>

<script>
import { faChevronRight } from '@fortawesome/free-solid-svg-icons';
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  data: function () {
    return {
      urlExtra: 'week/',
      faChevronRight,
    };
  },
  computed: {
    ...mapState({
      expLink: function (state) {
        return state.hx_toolkit.value[this.urlExtra].expLink;
      },
      srcset: function (state) {
        return state.hx_toolkit.value[this.urlExtra].srcset;
      },
      src: function (state) {
        return state.hx_toolkit.value[this.urlExtra].src;
      },
      alt: function (state) {
        return state.hx_toolkit.value[this.urlExtra].alt;
      },
      articleTeaserTitle: function (state) {
        return state.hx_toolkit.value[this.urlExtra].articleTeaserTitle;
      },
      articleTeaserBody: function (state) {
        return state.hx_toolkit.value[this.urlExtra].articleTeaserBody;
      },

      hxtViewer: (state) => state.user.affiliations.hxt_viewer,
      page: (state) => state.page,
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
    showError() {
      return this.statusCode !== 404;
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
@import '@/css/variables.scss';

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
    opacity: 1;
  }
  .myuw-huskyexp-body {
    top: 0;
    padding: 2px;
  }

  .myuw-teaser-title {
    color: black;
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
