<template>
  <li role="presentation" :class="titleItemClassComputed">
    <div class="select-parent">
      <select
        :id="'tab-' + panelId"
        ref="tab"
        v-model="option"
        role="tab"
        :class="titleLinkClassComputed"
        @change="changeOption"
        @keydown.left.prevent="$parent.$emit('moveActiveTabLeft')"
        @keydown.right.prevent="$parent.$emit('moveActiveTabRight')"
      >
        <option
          v-for="(opt, i) in optionsList"
          :key="i"
          :value="opt.value"
          :disabled="opt.disabled"
        >
          {{opt.text}}
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
      // must match uw-tab-panel panelId
      type: String,
      required: true
    },
    optionsList: {
      // list of dropdown options
      type: [String, Array, Object],
      required: true
    },
    selectedOption: {
      // initially selected option 
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
      // the tab is active if the parent's active panel id
      // matches the tab panel id
      return this.$parent.activePanelId == this.panelId
    },
    option: {
        get: function(){
          return this.selectedOption;
        },
        set: function(newValue){
          this.$emit('input', newValue);
        }   
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
      cls['pb-1'] = true;
      cls['pt-1'] = true;
      cls['h-100'] = true;
      cls['active'] = this.active;
      cls['text-body'] = true;
      cls['rounded-0'] = true;
      return cls;
    },
  },
  watch: {
    active: function() {
      if(this.active) {
        // bring the tab into focus
        this.$refs.tab.focus();
        // never allow disabled option to be active
        if (this.option == 0 && this.optionsList[0].disabled) {
          // set the selected option to the first option in the list
          this.$emit('input', 1);
        }
      } else {
        // reset dropdown to first option
        this.$emit('input', 0);
      }
    },
  },
  methods: {
    changeOption() {
      // when the selected dropdown option is changed, first set the
      // selected option and set the tab panel content to that option
      this.$parent.$emit('setActivePanel', this.panelId);
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