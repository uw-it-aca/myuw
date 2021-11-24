<template>
  <div :id="id" class="collapse">
    <slot />
  </div>
</template>

<script>
import { Collapse } from 'bootstrap';

export default {
  model: {
    prop: 'isOpen',
    event: 'toggled',
  },
  props: {
    id: {
      type: String,
      required: true,
    },
    isOpen: {
      type: Boolean,
      default: false,
    },
    // Should start visible?
    visible: {
      type: Boolean,
      default: false,
    }
  },
  data() {
    return {
      collapse: null,
    };
  },
  watch: {
    isOpen(newIsOpen) {
      if (!this.$el.classList.contains('collapsing')) {
        if (newIsOpen) {
          this.collapse.show();
        } else {
          this.collapse.hide();
        }
      }
      if (newIsOpen) {
        this.$emit('open');
        this.$emit('show');
      } else {
        this.$emit('close');
        this.$emit('hide');
      }
    },
    visible(newVisible) {
      if (this.collapse) { 
        if (newVisible) {
          this.collapse.show();
        } else {
          this.collapse.hide();
        }
      }
    },
  },
  mounted() {
    this.collapse = Collapse.getOrCreateInstance(
      this.$el,
      { toggle: this.visible || this.isOpen },
    );

    this.$el.addEventListener(
      'show.bs.collapse',
      () => this.$emit('toggled', true),
    );
    this.$el.addEventListener(
      'hide.bs.collapse',
      () => this.$emit('toggled', false),
    );
  },
};
</script>

<style lang="scss" scoped>
</style>