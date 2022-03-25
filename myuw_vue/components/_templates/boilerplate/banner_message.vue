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
  data: function() {
    return {
    };
  },
  props: {
    messages: {
      type: Object,
      required: true,
    },
  },
  computed: {
    groupedByLevel() {
      const data = {
        'Info': [],
        'Warning': [],
        'Danger': [],
        'Success': []
      };
      this.messages.forEach((msg, j) => {
          if (msg.level_name in data) {
              data[msg.level_name].push(msg)  
          }
      });       
      return data;
    },
    warningMsgs() {
      return this.groupedByLevel['Warning'];
    },
    dangerMsgs() {
      return this.groupedByLevel['Danger'];
    },
    infoMsgs() {
      return this.groupedByLevel['Info'];
    },
    successMsgs() {
      return this.groupedByLevel['Success'];
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
