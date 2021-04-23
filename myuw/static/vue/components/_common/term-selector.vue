<template>
  <b-tabs
    v-model="selectedTab"
    lazy
    pills
    nav-wrapper-class="mb-3 p-0"
    active-nav-item-class="bg-transparent rounded-0 myuw-border-bottom
      border-dark text-body font-weight-bold"
    @activate-tab="displayedTabChange"
  >
    <!--
      Only mounts the tab when it is selected, so the data should be
      fetched on mount for the components in here
     -->
    <b-tab
      v-for="(tab, i) in displayedTabs"
      :key="i"
      title-item-class="text-nowrap myuw-text-lg mr-2 mb-1"
      title-link-class="rounded-0 px-2 py-1 h-100 text-body myuw-border-bottom"
    >
      <template #title>
        {{ tab.quarter }} '{{ tab.year % 100 }}
      </template>
      <slot :tab="tab" />
    </b-tab>
    <b-tab
      title-item-class="ml-auto text-nowrap myuw-text-lg mr-2 mb-1"
      title-link-class="rounded-0 px-0 py-1 h-100 text-body myuw-border-bottom myuw-font-open-sans"
    >
      <template #title>
        <div class="form-select-parent">
          <b-form-select
            v-model="selectedOption"
            plain
            :options="dropdownTabsSelectable"
            @change="optionTabChange"
          />
          <font-awesome-icon :icon="faChevronDown" class="down-arrow"/>
        </div>
      </template>
      <slot :tab="dropdownTabs[selectedOption]" />
    </b-tab>
  </b-tabs>
</template>

<script>
import {
  faChevronDown,
} from '@fortawesome/free-solid-svg-icons';

export default {
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
    let displayedTabs = [
      this.allTabs[currentIndex],
      this.allTabs[currentIndex + 1],
      this.allTabs[currentIndex + 2],
    ];

    let dropdownTabs = this.allTabs.slice(0, -3).reverse();

    let dropdownTabsSelectable = dropdownTabs.map((tab, i) => {
      return {
        value: i + 1,
        text: `${tab.quarter} '${tab.year % 100}`,
      };
    });

    dropdownTabs.unshift('Prev. Terms');
    dropdownTabsSelectable.unshift({
      value: 0,
      text: 'Prev. Terms',
      disabled: true,
    });

    let selectedTab = 0;
    let selectedOption = 0;

    if (this.selectedTerm) {
      let i = displayedTabs.findIndex((tabData) =>
        `${tabData.year},${tabData.quarter.toLowerCase()}` === this.selectedTerm
      );
      if (i > -1) {
        selectedTab = i;
      } else {
        i = dropdownTabs.findIndex((tabData) =>
          `${tabData.year},${tabData.quarter.toLowerCase()}` === this.selectedTerm
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
    selectedTermInner(newValue, oldValue) {
      if (newValue !== oldValue) {
        this.$emit('selected', newValue);
        this.$logger.termSelected(newValue);
      }
    }
  },
  created() {
    this.$logger.termSelected(this.selectedTermInner);
  },
  methods: {
    displayedTabChange(newIndex, _prevIndex, bvEvent) {
      if (newIndex < 3) {
        this.selectedTermInner = this.displayedTabs[newIndex].label;
        this.selectedOption = 0;
      } else {
        if (this.selectedOption === 0) {
          bvEvent.preventDefault();
        }
      }
    },
    optionTabChange(index) {
      this.selectedTermInner = this.dropdownTabs[index].label;
      this.selectedTab = 3;
    }
  }
};
</script>

<style lang="scss" scoped>
select {
  &::-ms-expand {
    display: none;
  }

  &.form-control {
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
}

.form-select-parent {
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