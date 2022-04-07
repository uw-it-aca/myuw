<template>
  <div class="tabs">
    <div :class="navWrapperClassesComputed">
      <ul role="tablist" :class="navClassesComputed">
        <slot name="tabs">
          <!-- uw-tab-button and uw-tab-dropdown components with panelId-->
        </slot>
      </ul>
    </div>
    <div class="tab-content">
      <slot name="panels">
        <!-- uw-tab-panel components with panelId matching tabs-->
      </slot>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
export default {
  model: {
    // allows v-model binding on activeTabIdx
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
  data(){
    return {
      localIndex: this.activeTabIdx
    }
  },
  computed: {
    ...mapState({
      activeTabStored: (state) => state.activeTabStored,
    }),
    tabs() {
      // this is a check to remove any components in the scoped slot
      // that are undefined. Vue sometimes adds undefined components.
      var filtered = this.$scopedSlots.tabs();
      filtered = filtered.filter(record => {
          return record.tag
      });
      return filtered
    },
    index: {
      get: function(){
        return this.localIndex;
      },
      set: function(newValue){
        this.localIndex = newValue;
        this.$emit('selected', newValue);
      }   
    },
    activePanelId() {
      // currently visible panel
      return (this.activeTabStored ? this.activeTabStored :
        this.tabs[this.index].componentOptions.propsData.panelId);
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
  created() {
    this.$on("setActivePanel", (panelId) => {
      // child tab components emit setActivePanel when
      // a tab is activated
      this.setActivePanel(panelId);
    });
    this.$on("moveActiveTabLeft", () => {
      // on pressing the left keyboard key, shift the index left
      this.moveActiveTabLeft();
    });
    this.$on("moveActiveTabRight", () => {
      // on pressing the right keyboard key, shift the index right
      this.moveActiveTabRight();
    });
  },
  methods: {
    saveActiveTabInStore(id) {
      this.addVarToState({
        name: 'activeTabStored',
        value: id,
      });
    },
    setActivePanel: function(panelId) {
      // find the index of the tab with the specified panelId
      // and set it as the index
      let idx = 0;
      this.tabs.forEach((tab, i) => {
        if(tab.componentOptions &&
           tab.componentOptions.propsData.panelId == panelId) {
          idx = i
        }          
      });
      this.index = idx;
    },
    moveActiveTabLeft: function() {
      // move active tab to the left, not exceeding first tab
      if (this.index > 0) {
        this.index -= 1;
      }
    },
    moveActiveTabRight: function() {
      // move active tab to the right, not exceeding last tab
      if (this.index < this.tabs.length - 1) {
        this.index += 1;
      }
    },
    ...mapMutations([
      'addVarToState',
    ]),
  },
  watch: {
    index(newIndex) {
      this.saveActiveTabInStore(
        this.tabs[newIndex].componentOptions.propsData.panelId);
    }
  },
}
</script>
