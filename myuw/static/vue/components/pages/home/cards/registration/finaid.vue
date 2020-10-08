<template>
  <div>
    <h4>Financial Aid</h4>
    <ul>
      <li v-for="(notice, i) in finAidNotices" :key="i">
        <button
          v-b-toggle="`finAid-${notice.id_hash}-collapse`"
        >
          <font-awesome-icon
            v-if="collapseOpen"
            :icon="['fas', 'caret-down']"
          />
          <font-awesome-icon
            v-else
            :icon="['fas', 'caret-right']"
          />
          {{ notice.short_content }}
        </button>
        <b-collapse
          :id="`finAid-${notice.id_hash}-collapse`"
          v-model="collapseOpen"
          v-html="notice.notice_content"
        />
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

</style>
