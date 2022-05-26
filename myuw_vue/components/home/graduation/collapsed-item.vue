<template>
  <div>
    <div class="d-flex d-inline-flex notice-container">
      <div class="flex-grow-1 pe-1">
        <button
          v-uw-collapse="`graduation-${notice.id_hash}-collapse-${$meta.uid}`"
          v-no-track-collapse
          type="button"
          class="btn btn-link p-0 border-0 align-top notice-link text-start myuw-text-md"
        >
          <span class="notice-title" v-html="notice.notice_title" />
        </button>
      </div>
    <div>
      <span v-if="!notice.is_read" class="badge bg-warning fw-normal notice-status text-dark p-1">
      New
      </span>
    </div>
</div>
    <uw-collapse
      :id="`graduation-${notice.id_hash}-collapse-${$meta.uid}`"
      v-model="collapseOpen"
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
  data: function() {
    return {
      collapseOpen: false,
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
</style>
