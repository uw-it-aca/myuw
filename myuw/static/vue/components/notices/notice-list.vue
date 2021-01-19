<template>
  <div v-if="notices.length !== 0">
    <div v-b-toggle="collapseId">
      <div  class="d-flex">
        <h3>{{title}}</h3>
        <div class="ml-auto">
          <span v-if="unreadCount">
            {{unreadCount}} Unread
          </span>
          <font-awesome-icon v-if="!collapseOpen" :icon="faChevronDown" />
          <font-awesome-icon v-else :icon="faChevronUp" />
        </div>
      </div>
      <span v-if="!critical && criticalCount !== 0">
        {{criticalCount}} Critical
      </span>
    </div>
    <b-collapse :id="collapseId" ref="collapsible" v-model="collapseOpen">
      <div v-for="(notice, i) in notices" :key="i">
        <div class="d-flex">
          <div>{{notice.category}}</div>
          <div class="ml-auto">
            <span v-if="!notice.is_read">Unread</span>
            <font-awesome-icon v-if="notice.is_critical" :icon="faExclamationTriangle" />
          </div>
        </div>
        <h4>
          <div v-html="notice.notice_title" />
        </h4>
        <div v-html="notice.notice_body" />
        <button v-if="!notice.is_read" @click="onShowNotice(notice)">Mark Read</button>
      </div>
    </b-collapse>
  </div>
</template>

<script>
import {
  faChevronUp,
  faChevronDown,
  faExclamationTriangle
} from '@fortawesome/free-solid-svg-icons';
import {mapActions} from 'vuex';

export default {
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
    }
  },
  computed: {
    unreadCount() {
      return this.notices.filter((n) => !n.is_read).length;
    },
    criticalCount() {
      return this.notices.filter((n) => n.is_critical).length;
    }
  },
  methods: {
    onShowNotice(notice) {
      if (!notice.is_read) {
        this.setRead(notice);
      }
    },
    ...mapActions('notices', ['setRead']),
  },
}
</script>