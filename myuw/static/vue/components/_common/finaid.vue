<template>
  <div class="mt-4">
    <h3 class="h6 text-dark-beige myuw-font-encode-sans">
      Financial Aid
    </h3>
    <slot name="status" />
    <ul class="list-unstyled">
      <li v-for="(notice, i) in finAidNotices" :key="i">
        <button type="button"
          v-b-toggle="`finAid-${notice.id_hash}-collapse-${$meta.uid}`"
          v-no-track-collapse
          class="btn btn-link p-0 border-0 mb-2 bg-transparent myuw-text-md"
          size="md"
        >
          <font-awesome-icon v-if="collapseOpen[i]" :icon="faCaretDown" />
          <font-awesome-icon v-else :icon="faCaretRight" />
          <span v-html="notice.short_content" />
        </button>
        <b-collapse
          :id="`finAid-${notice.id_hash}-collapse-${$meta.uid}`"
          v-model="collapseOpen[i]"
          class="myuw-fin-aid"
          @show="onShowNotice(notice)"
        >
          <div
            class="bg-warning m-0 p-3 border-0 rounded-0 myuw-text-sm"
            v-html="notice.notice_body"
          />
        </b-collapse>
      </li>
    </ul>
  </div>
</template>

<script>
import {
  faCaretDown,
  faCaretRight,
} from '@fortawesome/free-solid-svg-icons';
import {mapActions} from 'vuex';
export default {
  props: {
    finAidNotices: {
      type: Array,
      required: true,
    },
  },
  data: function() {
    return {
      collapseOpen: Array(this.finAidNotices.length).fill(false),
      faCaretDown,
      faCaretRight,
    };
  },
  methods: {
    onShowNotice(notice) {
      this.$logger.noticeOpen(this, notice);
      if (!notice.is_read) {
        this.setRead(notice);
      }
    },
    ...mapActions('notices', ['setRead']),
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import '../../../css/myuw/variables.scss';
.myuw-fin-aid {
  // override warning background
  ::v-deep .bg-warning {
    background-color: lighten(
      map.get($theme-colors, 'warning'),
      47%
    ) !important;
  }

  ::v-deep .notice-title {
    font-weight: bold;
    display: block;
  }

  ::v-deep .date {
    font-weight: bold;
  }
}

span {
  ::v-deep .date {
    font-weight: bold;
  }
}
</style>
