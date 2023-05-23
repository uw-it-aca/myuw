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
};
</script>
