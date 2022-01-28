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
      cls['text-uppercase'] = true;
      cls['px-2'] = true;
      cls['py-1'] = true;
      cls['h-100'] = true;
      cls['active'] = this.active;
      return cls;
    },
  },
  watch: {
    active: function() {
      if(this.active)
        this.$refs.tab.focus();
    }
  },
  methods: {
    classesToClassDict(classes) {
      let classDict = {};
      if (classes instanceof String || typeof(classes) === 'string') {
        classes.split(/\s+/).forEach((c) => classDict[c] = true);
      } else if (classes instanceof Array) {
        classes.forEach((c) => classDict[c] = true);
      } else if (classes) {
        // Want to copy here?
        Object.entries(classes).forEach(([key, value]) => classDict[key] = value);
      }
      return classDict;
    },
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