<template>
  <div :id="'panel-' + panelId"
      role="tabpanel"
      :aria-labelledby="'tab-' + panelId"
      :class="tabPanelClassComputed">
    <slot></slot>
  </div>
</template>

<script>

export default {
  props: {
    panelId: {
      // must match tab panelId
      type: [String, Number],
      required: true
    }
  },
  computed: {
    active() {
      // the panel is active if the parent's active panel id
      // matches the panel's panel id
      return this.$parent.activePanelId == this.panelId
    },
    tabPanelClassComputed() {
      let tabPanelClass = {};
      tabPanelClass['tab-pane'] = true;
      tabPanelClass['fade'] = true;
      // toggle the visible tab using the active variable
      tabPanelClass['show'] = this.active;
      tabPanelClass['active'] = this.active;
      return tabPanelClass;
    },
  },
}
</script>