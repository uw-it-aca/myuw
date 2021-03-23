<template>
  <div class="mb-4">
    <div class="d-flex align-items-center mb-2">
      <h4 class="h6 m-0 text-dark font-weight-bold flex-fill">
        Holds
      </h4>
      <div :class="[!isMyPlanPeakLoad ? 'text-right' : '']" class="flex-fill">
        <font-awesome-icon
          :icon="['fas', 'exclamation-triangle']"
          class="mr-1 align-middle text-danger"
          aria-hidden="true"
        />
        <b-button
          v-b-toggle="`${summerCardLabel}holds-collapse-${$meta.uid}`"
          :title="buttonTitle"
          variant="link"
          class="p-0 border-0 text-danger font-weight-bold"
        >
          {{ regHoldsNotices.length }}
          {{ regHoldsNotices.length > 1 ? "holds" : "hold" }}
          <font-awesome-icon v-if="!collapseOpen" :icon="faChevronDown" />
          <font-awesome-icon v-else :icon="faChevronUp" />
        </b-button>
      </div>
    </div>
    <b-collapse
      :id="`${summerCardLabel}holds-collapse-${$meta.uid}`"
      v-model="collapseOpen"
      class="myuw-reg-holds"
    >
      <div class="bg-danger m-0 p-3 border-0 rounded-0">
        <h5 class="h6 font-weight-bold">
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
import {
  faChevronUp,
  faChevronDown,
} from '@fortawesome/free-solid-svg-icons';
export default {
  props: {
    summerCardLabel: {
      type: String,
      default: '',
    },
    regHoldsNotices: {
      type: Array,
      required: true,
    },
    isMyPlanPeakLoad: {
      type: Boolean,
      required: true,
    },
  },
  data: function() {
    return {
      collapseOpen: false,
      faChevronUp,
      faChevronDown,
    };
  },
  computed: {
    buttonTitle() {
      if (this.collapseOpen) return 'Collapse to hide holds details';
      return 'Expand to show holds details';
    },
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import "../../../../css/myuw/variables.scss";

.myuw-reg-holds {
  // override danger background
  .bg-danger {
    background-color: lighten(map.get($theme-colors, "danger"), 50%) !important;
  }
  .myuw-reg-holds-list {
    li {
      &:last-child { margin-top: 1rem;}
      // use ::v-deep for deep selection of embeded classes in scoped styles
      ::v-deep .notice-title {
        font-weight: bold;
        display: block;
      }
    }
  }
}
</style>
