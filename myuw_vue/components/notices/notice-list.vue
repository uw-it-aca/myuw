<template>
  <div v-if="notices.length !== 0" class="border-bottom py-3">
    <div v-uw-collapse="collapseId">
      <div :class="[title.includes('Critical') ? 'text-danger' : '']" class="d-flex py-1">
        <h2 class="h4 mb-0">
          {{ title }}
        </h2>
        <div class="ms-auto">
          <span
            v-if="unreadCount"
            :class="[title.includes('Critical') ? 'border-danger' : 'border-secondary']"
            class="me-2 border rounded-pill px-2 myuw-text-md"
          >
            {{ unreadCount }} new
          </span>
          <font-awesome-icon v-if="!collapseOpen" :icon="faChevronDown" class="align-middle" />
          <font-awesome-icon v-else :icon="faChevronUp" class="align-middle" />
        </div>
      </div>
      <span v-if="!critical && criticalCount !== 0" class="text-muted myuw-text-md">
        {{ criticalCount }} Critical
      </span>
    </div>
    <uw-collapse :id="collapseId" ref="collapsible" v-model="collapseOpen" class="mt-3">
      <div
        v-for="(notice, i) in sortNotices(notices)"
        :key="i"
        v-observe-visibility="observerConfig(notice)"
        :class="[$mq === 'desktop' ? 'w-75 mx-auto' : '']"
        class="bg-white mb-2 p-3"
      >
        <div class="d-flex">
          <div class="text-muted mb-2 myuw-text-md">{{ notice.category }}</div>
          <div class="ms-auto myuw-text-md">
            <span v-if="!notice.is_read" class="badge badge-warning fw-normal"
            >New</span>
            <font-awesome-icon
              v-if="notice.is_critical"
              :icon="faExclamationTriangle"
              class="text-danger"
            />
          </div>
        </div>
        <h3 class="h6 myuw-font-encode-sans" v-html="notice.notice_title" />
        <div class="myuw-text-md" v-html="notice.notice_body" />
      </div>
    </uw-collapse>
  </div>
</template>

<script>
import {
  faChevronUp,
  faChevronDown,
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';
import { mapActions } from 'vuex';
import Collapse from '../_templates/collapse.vue';

export default {
  components: {
    'uw-collapse': Collapse,
  },
  props: {
    notices: {
      type: Array,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    critical: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      collapseOpen: false,
      collapseId: Math.random().toString(),
      faChevronUp,
      faChevronDown,
      faExclamationTriangle,
    };
  },
  computed: {
    unreadCount() {
      return this.notices.filter((n) => !n.is_read).length;
    },
    criticalCount() {
      return this.notices.filter((n) => n.is_critical).length;
    },
  },
  methods: {
    observerConfig(notice) {
      return {
        callback: (isVisible, entry) => {
          if (isVisible) this.onNoticeVisible(notice, entry);
        },
        once: true,
        intersection: {
          threshold: 1.0,
        },
      };
    },
    onNoticeVisible(notice) {
      this.$logger.noticeOpen(this, notice);
      if (!notice.is_read) {
        this.setReadNoUpdate(notice);
      }
    },
    ...mapActions('notices', ['setReadNoUpdate']),
  },
};
</script>
<style lang="scss" scoped>
::v-deep .date {
  font-weight: bold;
}
</style>
