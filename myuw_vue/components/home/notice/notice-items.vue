<template>
  <ul class="list-unstyled mb-0 myuw-text-md">
    <li v-for="notice in notices" :key="notice.id_hash" class="mb-1">
      <uw-collapsed-item
        v-if="gradingOpen && isGradingNotice(notice)"
        :notice="notice" caller-id="noticeCard" :display-critical="true">
        <template #notice-body>
          Before grading begins, ...
        </template>
      </uw-collapsed-item>
      <uw-collapsed-item
        v-else
        :notice="notice" caller-id="noticeCard" :display-critical="true">
        <template #notice-body>
          <div v-html="notice.notice_body" />
        </template>
      </uw-collapsed-item>
    </li>
  </ul>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import CollapsedItem from '../../_common/collapsed-item.vue';

export default {
  components: {
    'uw-collapsed-item': CollapsedItem,
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
  computed: {
    ...mapState({
      gradingOpen: (state) => state.cardDisplayDates.within_grading_period,
    }),
  },
  methods: {
    onShowNotice(notice) {
      this.$logger.noticeOpen(this, notice);
      if (!notice.is_read) {
        this.setRead(notice);
      }
    },
    isGradingNotice(notice) {
      return notice.category.includes('GradingOpen');
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
