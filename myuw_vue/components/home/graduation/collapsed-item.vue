<template>
  <div>
    <div>
      <button
        v-uw-collapse="`graduation-${notice.id_hash}-collapse-${$meta.uid}`"
        v-no-track-collapse
        type="button"
        class="btn btn-link p-0 border-0 align-top notice-link text-start myuw-text-md"
      >
        <span class="notice-title" v-html="notice.notice_title" />
      </button>
      <span
        v-if="!notice.is_read"
        class="badge bg-warning fw-normal notice-status text-dark p-1"
      >New</span>
    </div>
    <uw-collapse
      :id="`graduation-${notice.id_hash}-collapse-${$meta.uid}`"
      tabindex="0"
      @show="onShowNotice(notice)"
    >
      <div class="p-3 mt-2 bg-light text-dark notice-body">
        <slot name="notice-body" />
      </div>
    </uw-collapse>
  </div>
</template>

<script>
import Collapse from '../../_templates/collapse.vue';
import {mapActions} from 'vuex';
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
  methods: {
    onShowNotice(notice) {
      alert(notice.notice_title);
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
</style>
