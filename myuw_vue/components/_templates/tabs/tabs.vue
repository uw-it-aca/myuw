<template>
  <div>
    <div :class="navWrapperClassesComputed">
      <ul role="tablist" :class="navClassesComputed">
        <li v-for="(item, idx) in $slots.default" :key="idx" :class="listItemClasses(item, idx)" role="presentation">
          <button ref="tabButton" role="tab" data-bs-toggle="tab" type="button" @click="activeTabIdx=idx" :class="buttonClasses(item, idx)" @keydown.left="moveActiveTabLeft" @keydown.right="moveActiveTabRight" :aria-selected="activeTabIdx === idx">
            {{item.componentOptions.propsData.title}}
          </button>
        </li>
      </ul>
    </div>
    <div class="tab-content">
      <slot></slot>
    </div>
  </div>
</template>

<script>

export default {
  model: {
    prop: 'tabIndex',
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
    tabIndex: {
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
  data() {
    return {
      activeTabIdx: 0,
    };
  },
  computed: {
    navWrapperClassesComputed() {
      let wrapperClasses = this.classesToClassDict(this.navWrapperClass);

      return wrapperClasses;
    },
    navClassesComputed() {
      let navClass = this.classesToClassDict(this.navClass);
      
      navClass['nav'] = true;

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

      navClass['myuw-tabs'] = true;
      navClass['myuw-bottom-border'] = this.bottomBorder;

      return navClass;
    },
  },
  created() {
    this.activeTabIdx = this.tabIndex;
  },
  watch: {
    activeTabIdx: function() {
      this.$refs.tabButton[this.activeTabIdx].focus()
    }
  },
  methods: {
    moveActiveTabLeft: function() {
      if (this.activeTabIdx > 0)
        this.activeTabIdx -= 1;
    },
    moveActiveTabRight: function() {
      if (this.activeTabIdx < this.$slots.default.length - 1)
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
    listItemClasses(item, idx) {
      let liClass =  this.classesToClassDict(item.componentOptions.propsData.titleItemClass);
      liClass['nav-item'] = true;
      return liClass;
    },
    buttonClasses(item, idx) {
      let buttonClass = this.classesToClassDict(item.componentOptions.propsData.titleLinkClass);
      buttonClass['nav-link'] = true;
      buttonClass['text-nowrap'] =true;
      buttonClass['text-uppercase'] = true;
      if (idx === this.activeTabIdx) {
        buttonClass['active'] = true;
      }
      return buttonClass;
    },
  },
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