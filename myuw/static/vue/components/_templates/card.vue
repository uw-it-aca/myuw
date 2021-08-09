<template>
  <div
    v-if="loaded"
    v-visibility-change="loaded ? visibilityChanged : null"
    class="card"
    :class="cardClasses"
  >
    <div class="card-body" :class="bodyClasses">
      <slot name="card-heading" />
      <div class="myuw-card-body">
        <slot name="card-body" />
      </div>
      <slot name="card-disclosure" />
    </div>
    <div v-if="!!$slots['card-footer']" class="card-footer border-0 px-3 py-2">
      <slot name="card-footer" />
    </div>

  </div>
  <div v-else-if="errored">
    <div v-if="erroredShow" class="card rounded-0 shadow-sm mb-3" tabindex="0">
      <div class="card-body p-3">
        <slot name="card-heading" />
        <!-- default card error message -->
        <div class="alert alert-light p-0 m-0 border-0 bg-transparent" role="alert">
          <div class="d-flex text-danger mb-3 myuw-text-md">
            <div class="pr-2 flex-shrink-1">
              <font-awesome-icon :icon="faExclamationTriangle" />
            </div>
            <div class="w-100">
              <slot name="card-error">
                An error has occurred and we can't load this content right now. Please try again
                later.
              </slot>
            </div>
          </div>
        </div>
        <slot name="card-error-extra"></slot>
      </div>
    </div>
  </div>
  <div v-else class="card rounded-0 shadow-sm mb-3">
    <div class="card-body p-3">
      <div class="card-text d-flex justify-content-center card-loading">
        <div class="spinner-border spinner-border-sm text-muted my-auto" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';

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
    ribbon: {
      type: Object,
      default: null,
    },
    noBottomMargin: {
      type: Boolean,
      default: false,
    },
  },
  data: function() {
    return {
      faExclamationTriangle,
    };
  },
  computed: {
    cardClasses() {
      const classes = {
        'rounded-0': true,
        'shadow-sm': true,
        'mb-3': !this.noBottomMargin,
      };
      return classes;
    },
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
      if (val) this.$logger.compLoad(this);
    },
  },
  created() {
    if (this.loaded) this.$logger.compLoad(this);
  },
  methods: {
    visibilityChanged(entry) {
      this.$logger.visibilityChanged(this, entry);
    },
  },
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

.myuw-card-body .card-property-group::v-deep {
  &:last-child .card-group-divider {
    display: none !important;
  }
}
</style>
