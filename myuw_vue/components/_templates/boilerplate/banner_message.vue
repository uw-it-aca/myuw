<template>
  <div class="message px-3 py-2 myuw-text-md">
    <ol class="list-unstyled">
      <li v-for="(level, l) in levels" :key="l">
        <ul class="styleAtLevel(level) list-unstyled">
          <li v-for="(msg, i) in messageAtLevel(level)" :key="i" class="mb-1">
            <span v-html="msg.content" />
          </li>
        </ul>
      </li>
    </ol>
  </div>
</template>

<script>
import {
} from '@fortawesome/free-solid-svg-icons';

export default {
  props: {
    messages: {
      type: Array,
      required: true,
    },
  },
  data: function() {
    return {
      levels: ['Warning', 'Info'],
    };
  },
  computed: {
    groupedMsgs() {
      const groupedByLevel = {
        'Info': [],
        'Warning': []
      };
      this.messages.forEach((msg, j) => {
        if (msg.level_name === 'Info' || msg.level_name === 'Success') {
          groupedByLevel['Info'].push(msg)
        } else {
          groupedByLevel['Warning'].push(msg)
        }
      });
      return groupedByLevel;
    },
  },
  methods: {
    messageAtLevel(level) {
      return this.groupedMsgs[level];
    },
    styleAtLevel(level) {
      return (level === 'Info' ? "msg-info" : "msg-warning");
    },
  }
}
</script>

<style lang="scss" scoped>
@use "sass:map";
@import '../../../../myuw/static/css/myuw/variables.scss';
.myuw-banner_message {
  ::v-deep .date {
    font-weight: bold;
  }

  ::v-deep .external-link {
    color: white;
  }

  ::v-deep .msg-warning {
    background-color: lighten(
      map.get($theme-colors, 'warning'),
      47%
    ) !important;
  }

  ::v-deep .msg-info {
    background-color: lighten(
      map.get($theme-colors, 'info'),
      47%
    ) !important;
  }
}
</style>
