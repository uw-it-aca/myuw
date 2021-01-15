<template>
  <b-tabs lazy :value="selectedTab">
    <!--
      Only mounts the tab when it is selected, so the data should be
      fetched on mount for the components in here
     -->
    <b-tab v-for="(tab, i) in displayedTabs" :key="i">
      <template #title>
        {{ tab.quarter }} '{{ tab.year % 100 }}
      </template>
      <slot :tab="tab" />
    </b-tab>
    <b-tab title-link-class="p-0">
      <template #title>
        <b-form-select
          v-model="selectedOption"
          :options="dropdownTabsSelectable"
        />
      </template>
      <slot :tab="dropdownTabs[selectedOption]" />
    </b-tab>
  </b-tabs>
</template>

<script>
export default {
  props: {
    currentYear: {
      type: Number,
      required: true,
    },
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
        value: i,
        text: `${tab.quarter} '${tab.year % 100}`,
      };
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

    return {
      selectedTab,
      selectedOption,
      displayedTabs,
      dropdownTabs,
      dropdownTabsSelectable,
    };
  },
};
</script>
