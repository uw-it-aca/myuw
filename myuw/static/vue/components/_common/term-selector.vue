<template>
  <b-tabs lazy>
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
          v-model="selected"
          :options="dropdownTabsSelectable"
        />
      </template>
      <slot :tab="dropdownTabs[selected]" />
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
  },
  data() {
    return {
      selected: 0,
    };
  },
  computed: {
    dropdownTabs() {
      // Remove the three tabs that are directly displayed
      return this.allTabs.slice(0, -3).reverse();
    },
    dropdownTabsSelectable() {
      return this.dropdownTabs.map((tab, i) => {
        return {
          value: i,
          text: `${tab.quarter} '${tab.year % 100}`,
        };
      });
    },
    displayedTabs() {
      const currentIndex = this.allTabs.findIndex((tab) =>
        tab.quarter.toLowerCase() == this.currentQuarter &&
        tab.year == this.currentYear,
      );
      return [
        this.allTabs[currentIndex],
        this.allTabs[currentIndex + 1],
        this.allTabs[currentIndex + 2],
      ];
    },
  },
};
</script>
