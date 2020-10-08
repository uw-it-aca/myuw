<template>
  <div>
    <div>
      <h4 v-if="myPlanData">
        Holds
      </h4>
      <div>
        <font-awesome-icon
          :icon="['fas', 'exclamation-triangle']"
          class="mr-1"
        />
        <button
          v-b-toggle="`${summerCardLabel}holds-collapse`"
          :title="buttonTitle"
        >
          <span v-if="collapseOpen">Hide</span>
          {{ regHoldsNotices.length }}
          {{ regHoldsNotices.length > 1 ? "holds" : "hold" }}
        </button>
      </div>
    </div>
    <b-collapse
      :id="`${summerCardLabel}holds-collapse`"
      v-model="collapseOpen"
    >
      <h4 class="sr-only">
        Registration and/or Transcript Holds
      </h4>
      <ul class="reg-holds-list">
        <li
          v-for="(notice, i) in regHoldsNotices"
          :key="i" v-html="notice.notice_content"
        />
      </ul>
    </b-collapse>
  </div>
</template>

<script>
export default {
  props: {
    myPlanData: {
      type: Object,
      default: null,
    },
    summerCardLabel: {
      type: String,
      default: '',
    },
    regHoldsNotices: {
      type: Array,
      required: true,
    },
  },
  data: function() {
    return {
      collapseOpen: false,
    };
  },
  computed: {
    buttonTitle() {
      if (this.collapseOpen) return 'Collapse and hide holds details';
      return 'Expand and show holds details';
    },
  },
};
</script>

<style lang="scss" scoped>

</style>
