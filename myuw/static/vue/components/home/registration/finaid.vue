<template>
  <div class="mt-4">
    <h4 class="h6 font-weight-bold">
      Financial Aid
    </h4>
    <ul class="list-unstyled m-0">
      <li v-for="(notice, i) in finAidNotices" :key="i">
        <b-button
          v-b-toggle="`finAid-${notice.id_hash}-collapse`"
          variant="link"
          class="p-0 border-0 mb-2 bg-transparent myuw-text-md"
          size="md"
        >
          <font-awesome-icon
            v-if="collapseOpen"
            :icon="['fas', 'caret-down']"
          />
          <font-awesome-icon v-else :icon="['fas', 'caret-right']" />
          {{ notice.short_content }}
        </b-button>
        <b-collapse
          :id="`finAid-${notice.id_hash}-collapse`"
          v-model="collapseOpen"
          class="myuw-fin-aid"
        >
          <div
            class="bg-warning m-0 p-3 border-0 rounded-0 myuw-text-sm"
            v-html="notice.notice_body"
          />
        </b-collapse>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    finAidNotices: {
      type: Array,
      required: true,
    },
  },
  data: function() {
    return {
      collapseOpen: false,
    };
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import '../../../../../css/myuw/variables.scss';
.myuw-fin-aid {
  // override warning background
  ::v-deep .bg-warning {
    background-color: lighten(
      map.get($theme-colors, 'warning'),
      47%
    ) !important;
  }

  ::v-deep .notice-title {
    font-weight: bold;
    display: block;
  }
}
</style>
