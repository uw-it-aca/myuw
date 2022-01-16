<template>
  <div ref="tab" role="tabpanel" aria-labelledby="todo" :class="tabPanelClassesComputed">
    <slot></slot>
  </div>
</template>

<script>

export default {
  props: {
    title: {
      type: String,
      default: '',
    },
    titleItemClass: {
      type: [String, Array, Object],
      default: '',
    },
    titleLinkClass: {
      type: [String, Array, Object],
      default: '',
    },
    titleItemIcon: {
      type: [String, Array, Object],
      default: undefined,
    }
  },
  computed: {
    active() {
      if (this.$parent) {
        let activeUid = this.$parent.validSlots[
          this.$parent.activeTabIdx].componentInstance.$meta.uid;
        return activeUid == this.$meta.uid;
      } else {
        return false;
      }
    },
    tabPanelClassesComputed() {
      let tabPanelClass = {};
      tabPanelClass['tab-pane'] = true;
      tabPanelClass['active'] = this.active;
      tabPanelClass['show'] = this.active;
      return tabPanelClass;
    },
  },
}
</script>