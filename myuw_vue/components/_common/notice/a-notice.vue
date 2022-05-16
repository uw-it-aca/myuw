<template>
  <div>
    <div class="d-flex d-sm-inline-flex notice-container">
      <div class="flex-grow-1 pe-1">
        <span class="notice-title">
          <button
            v-uw-collapse="notice.id_hash"
            v-no-track-collapse
            class="btn btn-link p-0 border-0 align-top notice-link text-start myuw-text-md"
          >
            <span
              v-if="notice.is_critical"
              class="d-inline-block fw-bold text-danger me-1 notice-critical"
              >Critical:</span
            ><span v-html="notice.notice_title" />
          </button>
        </span>
      </div>
      <div>
        <span
          v-if="!notice.is_read"
          class="badge bg-warning fw-normal notice-status text-dark p-1"
        >
          New
        </span>
      </div>
    </div>
    <uw-collapse :id="notice.id_hash" tabindex="0" @show="onShowNotice(notice)">
      <div class="p-3 mt-2 bg-light text-dark notice-body" v-html="notice.notice_body" />
    </uw-collapse>
  </div>
</template>

<script>
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';
import Collapse from '../../_templates/collapse.vue';

export default {
  components: {
    'uw-collapse': Collapse,
  },
  props: {
    notice: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      faExclamationTriangle,
    };
  },
  methods: {
    onShowNotice() {
      this.$logger.noticeOpen(this, notice);
      if (!notice.is_read) {
        this.setRead(notice);
      }
    },
  },
};
</script>
<style lang="scss" scoped>
::v-deep .date {
  font-weight: bold;
}
</style>
