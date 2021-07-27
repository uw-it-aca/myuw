<template>
  <div class="mb-4">
    <uw-card-status>
      <template #status-label>Holds</template>
      <template #status-value>
        <font-awesome-icon
          :icon="faExclamationTriangle"
          class="mr-1 align-middle text-danger"
          aria-hidden="true"
        />
        <button v-b-toggle="`${summerCardLabel}holds-collapse-${$meta.uid}`"
          type="button"
          class="btn btn-link btn-lg p-0 border-0 text-danger font-weight-bold"
        >
          {{ regHoldsNotices.length }}
          {{ regHoldsNotices.length > 1 ? 'holds' : 'hold' }}
          <font-awesome-icon v-if="!collapseOpen" :icon="faChevronDown" />
          <font-awesome-icon v-else :icon="faChevronUp" />
        </button>
      </template>
    </uw-card-status>
    <div :id="`${summerCardLabel}holds-collapse-${$meta.uid}`"
      v-model="collapseOpen"
      class="collapse myuw-reg-holds"
    >
      <div class="bg-danger m-0 p-3 border-0 rounded-0">
        <h4 class="h6 font-weight-bold">
          Registration and/or Transcript Holds
        </h4>
        <ul class="list-unstyled p-0 m-0 myuw-text-sm myuw-reg-holds-list">
          <li v-for="(notice, i) in regHoldsNotices" :key="i" v-html="notice.notice_content" />
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import CardStatus from '../../_templates/card-status.vue';
import {
  faChevronUp,
  faChevronDown,
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';

export default {
  components: {
    'uw-card-status': CardStatus,
  },
  props: {
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
      faChevronUp,
      faChevronDown,
      faExclamationTriangle,
    };
  },
  computed: {},
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import '../../../../css/myuw/variables.scss';

.myuw-reg-holds {
  // override danger background
  .bg-danger {
    background-color: lighten(map.get($theme-colors, 'danger'), 50%) !important;
  }
  .myuw-reg-holds-list {
    li {
      &:last-child {
        margin-top: 1rem;
      }
      // use ::v-deep for deep selection of embeded classes in scoped styles
      ::v-deep .notice-title {
        font-weight: bold;
        display: block;
      }
    }
  }
}
</style>
