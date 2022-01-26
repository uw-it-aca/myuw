<template>
  <div class="tabs">
    <div :class="navWrapperClassesComputed">
      <ul role="tablist" :class="navClassesComputed">
        <slot name="tabs"></slot>
      </ul>
    </div>
    <div class="tab-content">
      <slot name="panels"></slot>
    </div>
  </div>
</template>

<script>

export default {
  model: {
    prop: 'activeTabIdx',
    event: 'selected'
  },
  props: {
    navClass: {
      type: [String, Array, Object],
      default: '',
    },
    navWrapperClass: {
      type: [String, Array, Object],
      default: '',
    },
    activeTabIdx: {
      type: Number,
      default: 0,
    },
    justified: {
      type: Boolean,
      default: false,
    },
    small: {
      type: Boolean,
      default: false,
    },
    pills: {
      type: Boolean,
      default: false,
    },
    bottomBorder: {
      type: Boolean,
      default: false,
    },
  },
  created() {
    this.$on("setActivePanel", (panelId) => {
      this.setActivePanel(panelId);
    });
    this.$on("moveActiveTabLeft", () => {
      this.moveActiveTabLeft();
    });
    this.$on("moveActiveTabRight", () => {
      this.moveActiveTabRight();
    });
  },
  computed: {
    tabs() {
      var filtered = this.$scopedSlots.tabs();
      filtered = filtered.filter(record => {
          return record.tag
      });
      return filtered
    },
    activeTab() {
      return this.tabs[this.activeTabIdx];
    },
    activePanelId() {
      return this.tabs[this.activeTabIdx].componentOptions.propsData.panelId
    },
    navWrapperClassesComputed() {
      let wrapperClasses = this.classesToClassDict(this.navWrapperClass);
      return wrapperClasses;
    },
    navClassesComputed() {
      let navClass = this.classesToClassDict(this.navClass);
      navClass['nav'] = true;
      navClass['myuw-tabs'] = true;
      if (this.pills) {
        navClass['nav-pills'] = true;
        navClass['nav-tabs'] = false;
      } else {
        navClass['nav-tabs'] = true;
        navClass['nav-pills'] = false;
      }
      if (this.justified) {
        navClass['nav-justified'] = true;
      }
      if (this.small) {
        navClass['small'] = true;
      }
      if (this.bottomBorder) {
        navClass['myuw-bottom-border'] = true;
      }
      return navClass;
    },
  },
  methods: {
    setActivePanel: function(panelId) {
      let idx = 0;
      this.tabs.forEach((tab, i) => {
        if(tab.componentOptions &&
           tab.componentOptions.propsData.panelId == panelId) {
          idx = i
        }          
      });
      this.activeTabIdx = idx;
    },
    moveActiveTabLeft: function() {
      if (this.activeTabIdx > 0)
        this.activeTabIdx -= 1;
    },
    moveActiveTabRight: function() {
      if (this.activeTabIdx < this.tabs.length - 1)
        this.activeTabIdx += 1;
    },
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
  },
  watch: {
    activeTabIdx() {
      this.$emit('selected', this.activeTabIdx);
    },
  }
}
</script>