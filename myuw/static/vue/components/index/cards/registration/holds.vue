<template>
  <div class="mb-4">
    <div class="d-flex align-items-center mb-2">
      <h4 v-if="myPlanData" class="h6 m-0 text-dark flex-fill">
        Holds
      </h4>
      <div class="flex-fill text-right">
        <font-awesome-icon
          :icon="['fas', 'exclamation-triangle']"
          class="mr-1 align-middle text-danger"
          aria-hidden="true"
        />
        <b-button
          v-b-toggle="`${summerCardLabel}holds-collapse`"
          :title="buttonTitle"
          variant="link"
          class="p-0 border-0 text-danger font-weight-bold"
        >
          <span v-if="collapseOpen">Hide</span>
          {{ regHoldsNotices.length }}
          {{ regHoldsNotices.length > 1 ? "holds" : "hold" }}
        </b-button>
      </div>
    </div>
    <b-collapse
      :id="`${summerCardLabel}holds-collapse`"
      v-model="collapseOpen"
      class=""
    >
      <div class="alert alert-danger m-0 border-0 rounded-0 text-body">
        <h5 class="sr-only">
          Registration and/or Transcript Holds
        </h5>
        <ul class="list-unstyled p-0 m-0 myuw-text-sm myuw-reg-holds-list">
          <li
            v-for="(notice, i) in regHoldsNotices"
            :key="i" v-html="notice.notice_content"
          />
        </ul>
      </div>
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

<style lang="scss">
.myuw-reg-holds-list {
  li {
    &:last-child { margin-top: 1rem;}
    .notice-title { display: block; font-weight: bold;}
  }
}
</style>
