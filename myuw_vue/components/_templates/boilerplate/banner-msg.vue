<template>
  <div class="message px-0 py-0 myuw-text-md">
    <div v-for="(level, l) in levels" :key="l">
      <div :class="styleAtLevel(level)" class="list-unstyled">
        <div v-for="(msg, i) in messageAtLevel(level)" :key="i" class="px-3 py-2">
          <span v-html="msg.content" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {} from '@fortawesome/free-solid-svg-icons';

export default {
  props: {
    messages: {
      type: Array,
      required: true,
    },
  },
  data: function () {
    return {
      levels: ['Warning', 'Info'],
    };
  },
  computed: {
    groupedMsgs() {
      const groupedByLevel = {
        Info: [],
        Warning: [],
      };
      this.messages.forEach((msg, j) => {
        if (msg.level_name === 'Info' || msg.level_name === 'Success') {
          groupedByLevel['Info'].push(msg);
        } else {
          groupedByLevel['Warning'].push(msg);
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
      return level === 'Info' ? 'msg-info' : 'msg-warning';
    },
  },
};
</script>

<style lang="scss" scoped>
@use 'sass:map';
@import '@/css/variables.scss';
.message {
  ::v-deep .date {
    font-weight: bold;
  }

  ::v-deep .msg-info {
    background-color: map.get($theme-colors, 'dark-beige');
    color: white;
    .external-link {
      color: white;
      text-decoration: underline;
      &:hover {
        color: map.get($theme-colors, 'beige');
        }
    }
  }
  ::v-deep .msg-warning {
    background-color: map.get($theme-colors, 'warning') !important;
    color: black;

    .external-link {
    text-decoration: underline;
    color: black;
      &:hover {
      color: #555;
      }
    }
  }

}
</style>
