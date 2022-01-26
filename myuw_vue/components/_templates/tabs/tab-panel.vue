<template>
  <div :id="'panel-' + panelId" :aria-labelledby="'tab-' + panelId" :class="tabPanelClassComputed" role="tabpanel">
    <slot></slot>
  </div>
</template>

<script>

export default {
  props: {
    panelId: {
      type: [String, Number]
    }
  },
  computed: {
    active() {
      return this.$parent.activePanelId == this.panelId
    },
    tabPanelClassComputed() {
      let tabPanelClass = {};
      tabPanelClass['tab-pane'] = true;
      tabPanelClass['fade'] = true;
      tabPanelClass['show'] = this.active;
      tabPanelClass['active'] = this.active;
      return tabPanelClass;
    },
  },
}
</script>