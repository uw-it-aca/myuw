<template>
  <div v-if="(mobileOnly && $mq === 'mobile') || !mobileOnly">
    <b-card v-if="loaded"
            v-visibility-change="loaded ? visibilityChanged : null"
            class="rounded-0 shadow-sm mb-3"
            :body-class="bodyClasses"
            footer-class="border-0 px-3 py-2"
    >
      <slot name="card-heading" />
      <slot name="card-body" />
      <slot name="card-disclosure" />
      <template v-if="!!$slots['card-footer']"
                #footer
                footer-tag="footer"
      >
        <slot name="card-footer" />
      </template>
    </b-card>
    <div v-else-if="errored">
      <b-card v-if="erroredShow"
              class="rounded-0 shadow-sm mb-3" tabindex="0" body-class="p-3"
      >
        <slot name="card-heading" />

        <!-- default card error message -->
        <b-alert show variant="light" class="p-0 m-0 border-0 bg-transparent">
          <div class="d-flex text-danger mb-3 myuw-text-md">
            <div class="pr-2 flex-shrink-1">
              <font-awesome-icon :icon="['fas', 'exclamation-triangle']" />
            </div>
            <div class="w-100">
              <slot name="card-error">
                An error has occurred and we can't load this content right now.
                Please try again later.
              </slot>
            </div>
          </div>
        </b-alert>
        <slot name="card-error-extra"></slot>
      </b-card>
    </div>
    <b-card v-else class="rounded-0 shadow-sm mb-3" body-class="p-3">
      <b-card-text class="d-flex justify-content-center card-loading">
        <!-- TODO: replace this with a cog -->
        <b-spinner small variant="muted" class="my-auto" label="Loading..." />
      </b-card-text>
    </b-card>
  </div>
</template>

<script>
export default {
  props: {
    loaded: {
      type: Boolean,
      default: false,
    },
    errored: {
      type: Boolean,
      default: false,
    },
    erroredShow: {
      type: Boolean,
      default: true,
    },
    mobileOnly: {
      type: Boolean,
      default: false,
    },
    ribbon: {
      type: Object,
      default: null,
    },
  },
  data: function() {
    return {};
  },
  computed: {
    bodyClasses() {
      const classes = {
        'p-3': true,
      };

      if (this.ribbon && this.ribbon.side && this.ribbon.colorId) {
        classes['myuw-ribbon'] = true;
        classes[`myuw-ribbon-${this.ribbon.side}`] = true;
        classes[`myuw-ribbon-c${this.ribbon.colorId}`] = true;
      }

      return classes;
    },
  },
  watch: {
    loaded(val) {
      if (val) this.$logger.cardLoad(this);
    },
  },
  created() {
    if (this.loaded) this.$logger.cardLoad(this);
  },
  methods: {
    visibilityChanged(entry) {
      this.$logger.visibilityChanged(this, entry);
    }
  }
};
</script>

<style lang="scss" scoped>
.card-overlay {
  position: absolute;
  height: 100px;
  width: calc(100% - 20px);
  background-color: rgba(1, 1, 1, 0.5);
  z-index: 9999;
  color: white;
}
</style>