<template>
  <ul v-else class="list-unstyled mb-0 myuw-text-md">
    <li v-for="(notice, i) in sortNotices(notices)" :key="notice.id_hash" class="mb-1">
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
      <uw-collapse
        :id="notice.id_hash"
        v-model="noticeOpen[i]"
        tabindex="0"
        @show="onShowNotice(notice)"
      >
        <div class="p-3 mt-2 bg-light text-dark notice-body" v-html="notice.notice_body" />
      </uw-collapse>
    </li>
  </ul>
</template>

<script>
import { mapActions } from 'vuex';
import Collapse from '../../_templates/collapse.vue';

export default {
  components: {
    'uw-collapse': Collapse,
  },
  props: {
    notices: {
      type: Array,
      required: true,
    },
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
    ...mapActions('notices', ['fetch', 'setRead']),
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
