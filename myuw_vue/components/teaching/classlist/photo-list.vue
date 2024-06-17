<template>
  <div id="classlist_photo_view"
       class=""
       aria-labelledby="photo-grid"
  >
    <h3 class="visually-hidden">
      Grid of Student Photos
    </h3>
    <div class="sort-buttons">
      <button @click="setSortKey('first_name')">Sort by First Name</button>
      <button @click="setSortKey('surname')">Sort by Surname</button>
    </div>
    <ol class="list-unstyled d-flex flex-wrap">
      <li v-for="(reg, i) in sortedRegistrations"
          :id="`student-photo-${reg.regid}`"
          :key="i"
          class="p-1 mb-1"
          :class="reg.isJoint ? (showJointCourseStud ? 'd-inline' : 'd-none') : 'd-inline'"
      >
        <div v-lazyload style="width: 120px">
          <img :data-url="reg.photo_url"
              class=""
              width="120px" height="150px"
          >
          <strong>{{ reg.first_name }} {{ reg.surname }}</strong>
          <div class="myuw-text-sm">{{ reg.pronouns }}</div>
        </div>
      </li>
    </ol>
  </div>
</template>
<script>
import LazyLoad from "../../../directives/lazyload.js";
export default {
  directives: {
    lazyload: LazyLoad,
  },
  props: {
    registrations: {
      type: Array,
      required: true,
    },
    showJointCourseStud: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      sortKey: 'first_name',
    };
  },
  computed: {
    sortedRegistrations() {
      return [...this.registrations].sort((a, b) => {
        if (a[this.sortKey] < b[this.sortKey]) return -1;
        if (a[this.sortKey] > b[this.sortKey]) return 1;
        return 0;
      });
    },
  },
  methods: {
    setSortKey(key) {
      this.sortKey = key;
    },
  },
};
</script>
