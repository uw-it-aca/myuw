<template>
  <ul class="list-unstyled mb-0 myuw-text-md">
    <li v-for="notice in notices" :key="notice.id_hash" class="mb-1">
      <uw-collapsed-notice
        :notice="notice" caller-id="noticeCard" :display-critical="true">
        <template #notice-body>
          <div v-html="notice.notice_body" />
        </template>
      </uw-collapsed-notice>
    </li>
  </ul>
</template>

<script>
import { mapActions } from 'vuex';
import CollapsedNotice from '../../_common/collapsed-notice.vue';

export default {
  components: {
    'uw-collapsed-notice': CollapsedNotice,
  },
  props: {
    notices: {
      type: Array,
      required: true,
    },  // sorted by notice.sortDate
  },
  data() {
    return {
      noticeOpen: Array(this.notices.length).fill(false),  // MUWM-5147
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
@import '../../../../myuw/static/css/myuw/variables.scss';
::v-deep .date {
  font-weight: bold;
}
</style>
