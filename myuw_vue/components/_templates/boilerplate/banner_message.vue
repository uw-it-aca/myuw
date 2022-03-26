<template>
  <div class="myuw-text-md">
    <div v-if="dangerMsgs.length" class="bg-danger">
      <ul class="list-unstyled">
        <li v-for="(msg, i) in dangerMsgs" :key="i" class="mb-1">
          <span v-html="msg.content" />
        </li>
      </ul>
    </div>
    <div v-if="warningMsgs.length" class="bg-warning">
      <ul class="list-unstyled">
        <li v-for="(msg, j) in warningMsgs" :key="j">
          <span v-html="msg.content" />
        </li>
      </ul>
    </div>
    <div v-if="infoMsgs.length" class="bg-info">
      <ul class="list-unstyled">
        <li v-for="(msg, k) in infoMsgs" :key="k">
          <span v-html="msg.content" />
        </li>
      </ul>
    </div>
    <div v-if="successMsgs.length" class="bg-success">
      <ul class="list-unstyled">
        <li v-for="(msg, l) in successMsgs" :key="l">
          <span v-html="msg.content" />
        </li>
      </ul>
    </div>
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
      grouped:false,
      groupedByLevel: {
        'Info': [],
        'Warning': [],
        'Danger': [],
        'Success': []
      },
    };
  },
  computed: {
    groupedMsgs() {
      if (!this.grouped) {
        this.messages.forEach((msg, j) => {
          if (msg.level_name in this.groupedByLevel) {
            this.groupedByLevel[msg.level_name].push(msg)
          }
        });
        this.grouped = true;
      }
      return this.groupedByLevel;
    },
    warningMsgs() {
      return this.groupedMsgs['Warning'];
    },
    dangerMsgs() {
      return this.groupedMsgs['Danger'];
    },
    infoMsgs() {
      return this.groupedMsgs['Info'];
    },
    successMsgs() {
      return this.groupedMsgs['Success'];
    },
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import '../../../../myuw/static/css/myuw/variables.scss';
.myuw-banner_message {
  ::v-deep .external-link {}

  ::v-deep .bg-danger {
    background-color: lighten(
      map.get($theme-colors, 'danger'),
      47%
    ) !important;
  }
  
  ::v-deep .bg-warning {
    background-color: lighten(
      map.get($theme-colors, 'warning'),
      47%
    ) !important;
  }

  ::v-deep .bg-info {
    background-color: lighten(
      map.get($theme-colors, 'info'),
      47%
    ) !important;
  }

  ::v-deep .bg-success {
    background-color: lighten(
      map.get($theme-colors, 'primary'),
      47%
    ) !important;
  }
}
</style>
