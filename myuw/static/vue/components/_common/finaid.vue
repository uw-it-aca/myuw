<template>
  <div class="mt-4">
    <h4 class="h6 font-weight-bold text-dark-beige">
      Financial Aid
    </h4>
    <slot name="status" />
    <ul class="list-unstyled">
      <li v-for="(notice, i) in finAidNotices" :key="i">
        <b-button
          v-b-toggle="`finAid-${notice.id_hash}-collapse-${$meta.uid}`"
          v-no-track-collapse
          variant="link"
          class="p-0 border-0 mb-2 bg-transparent myuw-text-md"
          size="md"
        >
          <font-awesome-icon
            v-if="collapseOpen[i]"
            :icon="['fas', 'caret-down']"
          />
          <font-awesome-icon v-else :icon="['fas', 'caret-right']" />
          <span v-html="notice.short_content" />
        </b-button>
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
    };
  },
  methods: {
    onShowNotice(notice) {
      this.$logger.noticeOpen(this, notice);
    },
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
}

span {
  ::v-deep .date {
    font-weight: bold;
  }
}
</style>
