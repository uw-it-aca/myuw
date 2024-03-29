<template>
  <uw-tabs
    v-model="selectedTab"
    pills
    bottom-border
    :nav-wrapper-class="['mb-3', $mq === 'mobile' ? 'px-2' : 'p-0']"
  >
    <!--
      Only mounts the tab when it is selected, so the data should be
      fetched on mount for the components in here
     -->
    <template #tabs>
      <uw-tab-button
        v-for="(tab, i) in displayedTabs"
        :key="i"
        :panel-id="panleId(tab)"
        title-item-class="text-nowrap myuw-text-lg me-2 mb-1"
        title-link-class="rounded-0 px-2 py-1 h-100 text-body"
      >
        {{ tab.quarter + " '" + (tab.year % 100) }}
      </uw-tab-button>
      <uw-tab-dropdown
        v-if="dropdownTabs.length > 1"
        v-model="selectedOption"
        panel-id="dropdown"
        :options-list="dropdownTabsSelectable"
        :title-item-class="{
          'ms-auto': $mq !== 'mobile',
          'text-nowrap': true,
          'myuw-text-lg': true
        }"
      >
      </uw-tab-dropdown>
    </template>
    <template #panels>
      <uw-tab-panel
          v-for="(tab, i) in displayedTabs"
          :key="i"
          :panel-id="panleId(tab)">
        <slot :tab="tab" />
      </uw-tab-panel>
      <uw-tab-panel v-if="selectedOption > 0" panel-id="dropdown">
        <slot :tab="dropdownTabs[selectedOption]" />
      </uw-tab-panel>
    </template>
  </uw-tabs>
</template>

<script>
import {
  faChevronDown,
} from '@fortawesome/free-solid-svg-icons';
import Tabs from '../_templates/tabs/tabs.vue';
import TabButton from '../_templates/tabs/button.vue';
import TabDropdown from '../_templates/tabs/dropdown.vue';
import TabPanel from '../_templates/tabs/panel.vue';

export default {
  components: {
    'uw-tabs': Tabs,
    'uw-tab-button': TabButton,
    'uw-tab-dropdown': TabDropdown,
    'uw-tab-panel': TabPanel,
  },
  model: {
    prop: 'selectedTerm',
    event: 'selected'
  },
  props: {
    // Current here means the year right now not the selected year
    currentYear: {
      type: Number,
      required: true,
    },
    // Current here means the quarter right now not the selected quarter
    currentQuarter: {
      type: String,
      required: true,
    },
    allTabs: {
      type: Array,
      required: true,
    },
    selectedTerm: {
      type: String,
      default: null,
    }
  },
  data() {
    const currentIndex = this.allTabs.findIndex((tab) =>
      tab.quarter.toLowerCase() == this.currentQuarter &&
      tab.year == this.currentYear,
    );
    // Bug on Mac OS:
    // 1. Click on Past Terms, click somewhere else to close the dropdown.
    // 2. Click on the Past terms again. can't select in the dropdown
    let displayedTabs = this.allTabs.slice(currentIndex, currentIndex + 3);
    let dropdownTabs = this.allTabs.slice(0, -3).reverse();
    let dropdownTabsSelectable = dropdownTabs.map((tab, i) => {
      return {
        value: i + 1,
        text: `${tab.quarter} '${tab.year % 100}`,
      };
    });
    dropdownTabs.unshift({label: 'Past Terms'});
    dropdownTabsSelectable.unshift({
      value: 0,
      text: 'Past Terms',
      disabled: true,
    });
    let selectedTab = 0;
    let selectedOption = 0;
    if (this.selectedTerm) {
      let i = displayedTabs.findIndex((tabData) =>
        `${tabData.year},${tabData.quarter?.toLowerCase()}` === this.selectedTerm
      );
      if (i > -1) {
        selectedTab = i;
      } else {
        i = dropdownTabs.findIndex((tabData) =>
          `${tabData.year},${tabData.quarter?.toLowerCase()}` === this.selectedTerm
        );
        if (i > -1) {
          selectedOption = i;
          selectedTab = 3;
        }
      }
    }
    let selectedTermInner = this.selectedTerm;
    if (!selectedTermInner) {
      if (selectedTab < 3) {
        selectedTermInner = displayedTabs[selectedTab].label;
      } else {
        selectedTermInner = dropdownTabs[selectedOption].label;
      }
    }
    return {
      selectedTab,
      selectedOption,
      selectedTermInner,
      displayedTabs,
      dropdownTabs,
      dropdownTabsSelectable,
      faChevronDown,
    };
  },
  watch: {
    selectedOption(newValue, oldValue) {
      this.updateSelectedTerm();
    },
    selectedTab() {
      this.updateSelectedTerm();
    },
    selectedTermInner(newValue, oldValue) {
      this.$emit('selected', newValue);
      this.$logger.termSelected(newValue);
    },
  },
  created() {
    this.$logger.termSelected(this.selectedTermInner);
  },
  methods: {
    updateSelectedTerm() {
      if (this.selectedTab < 3) {
        this.selectedTermInner = this.displayedTabs[this.selectedTab].label;
      } else {
        this.selectedTermInner = this.dropdownTabs[this.selectedOption].label;
      }
    },
    panleId(tab) {
      return tab.quarter + (tab.year % 100);
    },
  },
};
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
</style>