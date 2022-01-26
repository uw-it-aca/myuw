<template>
  <li role="presentation" :class="titleItemClassComputed">
    <div class="select-parent">
      <select
        :id="'tab-' + panelId"
        ref="tab"
        v-model="selectedOption"
        role="tab"
        :class="titleLinkClassComputed"
        @change="changeOption"
        @keydown.left.prevent="$parent.$emit('moveActiveTabLeft')"
        @keydown.right.prevent="$parent.$emit('moveActiveTabRight')"
      >
        <option
          v-for="(option, i) in optionsList"
          :key="i"
          :value="option.value"
          :disabled="option.disabled"
        >
          {{option.text}}
        </option>
      </select>
      <font-awesome-icon :icon="faChevronDown" class="down-arrow"/>
    </div>
  </li>
</template>

<script>

import {
  faChevronDown,
} from '@fortawesome/free-solid-svg-icons';

export default {
  model: {
    prop: 'selectedOption',
    event: 'input'
  },
  props: {
    panelId: {
      type: String,
      required: true
    },
    optionsList: {
      type: [String, Array, Object],
      required: true
    },
    selectedOption: {
      type: [String, Number, Object],
      default: 0
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
  data: function () {
    return {
      faChevronDown: faChevronDown
    };
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
      cls['rounded-0'] = true;
      cls['pb-1'] = true;
      cls['pt-1'] = true;
      cls['h-100'] = true;
      cls['text-body'] = true;
      cls['myuw-font-open-sans'] = true;
      cls['active'] = this.active;
      return cls;
    },
  },
  watch: {
    active: function() {
      if(this.active) {
        this.$refs.tab.focus();
        if (this.selectedOption == 0 && this.optionsList[0].disabled) {
          // never allow disabled option to be active
          this.$emit('input', 1);
        }
      } else {
        // reset dropdown
        this.$emit('input', 0);
      }
    },
  },
  methods: {
    changeOption() {
      this.$emit('input', this.selectedOption);
      this.$parent.$emit('setActivePanel', this.panelId);
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
  }
}
</script>

<style lang="scss" scoped>
select {
  &::-ms-expand {
    display: none;
  }
  -webkit-appearance: none; 
  appearance: none;
  background: initial;
  border: initial;
  border-radius: inherit;
  padding: 0;
  font-size: inherit;
  text-transform: inherit;
  color: inherit;
  cursor: pointer;
  padding-left: 0.5rem;
  padding-right: 2.0rem;
}
.select-parent {
  position: relative;
  .down-arrow {
    position: absolute;
    right: 0.5rem;
    top: 0.36rem;
    z-index: 1;
    pointer-events: none;
  }
}
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