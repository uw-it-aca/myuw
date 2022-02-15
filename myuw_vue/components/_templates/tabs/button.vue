<template>
  <li role="presentation" :class="titleItemClassComputed">
    <button
      :id="'tab-' + panelId"
      ref="tab"
      :aria-controls="'panel-' + panelId"
      :area-selected="active"
      :class="titleLinkClassComputed"
      :data-bs-target="'#panel-' + panelId"
      type="button"
      role="tab"
      data-bs-toggle="tab"
      @click="$parent.$emit('setActivePanel', panelId)"
      @keydown.left.prevent="$parent.$emit('moveActiveTabLeft')"
      @keydown.right.prevent="$parent.$emit('moveActiveTabRight')">
        <slot></slot>
    </button>
  </li>
</template>

<script>

export default {
  props: {
    panelId: {
      // must match uw-tab-panel panelId
      type: [String, Number],
      required: true
    },
    titleItemClass: {
      type: [String, Array, Object],
      default: '',
    },
    titleLinkClass: {
      type: [String, Array, Object],
      default: '',
    },
  },
  computed: {
    active() {
      // the tab is active if the parent's active panel id
      // matches the tab panel id
      return this.$parent.activePanelId == this.panelId
    },
    titleItemClassComputed() {
      let cls = this.classesToClassDict(this.titleItemClass);
      cls['nav-item'] = true;
      return cls;
    },
    titleLinkClassComputed() {
      let cls = this.classesToClassDict(this.titleLinkClass);
      cls['nav-link'] = true;
      cls['text-nowrap'] = true;
      cls['px-2'] = true;
      cls['py-1'] = true;
      cls['h-100'] = true;
      cls['active'] = this.active;
      return cls;
    },
  },
  watch: {
    active: function() {
      // bring the tab into focus
      if(this.active)
        this.$refs.tab.focus();
    }
  }
}
</script>


<style lang="scss" scoped>
.myuw-tabs {
  .nav-link.active { 
    background: transparent;
    font-weight: bold;
  }
}
.myuw-bottom-border {
  .nav-link { border-bottom: 0.3125rem solid #ddd; }
  .nav-link.active {
    border-bottom-color: #000;
  }
}
</style>