<template>
  <div id="classlist_photo_view"
       class=""
       aria-labelledby="photo-grid"
  >
    <h3 class="visually-hidden">
      Grid of Student Photos
    </h3>
    <!--div class="sort-buttons myuw-text-md">
      <span class="py-1" style=""><strong>Sort by:</strong></span><button
        v-for="field in fields"
        :key="field.key"
        type="button"
        :class="buttonClass(field.key)"
        @click="setSortKey(field.key)"
      >
        {{ field.label }}
      </button>
    </div -->
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
      sortKey: 'surname',
      fields: [
        { key: 'first_name', label: 'first name', sortable: true },
        { key: 'surname', label: 'last name', sortable: true }
      ]
    };
  },
  computed: {
    sortedRegistrations() {
      const key = this.sortKey;
      return [...this.registrations].sort((a, b) => {
        if (a[key] < b[key]) return -1;
        if (a[key] > b[key]) return 1;
        return 0;
      });
    },
  },
  methods: {
    setSortKey(key) {
      this.sortKey = key;
    },
    buttonClass(key) {
      return {
        'btn': true,
        'btn-link': true,
        'active': this.sortKey === key,
        'inactive': this.sortKey !== key,
        'disabled': this.sortKey === key,
        'myuw-text-md': true,
        'px-1': true,
        'py-1': true
      };
    }
  }
};
</script>
<style scoped>
.sort-buttons{
  padding-bottom:.5em;
}
.active {
  font-weight: bold;
}
.inactive {
  font-weight: normal;
}
.btn-link.disabled {
  color: #000;
  opacity:1;
}
  </style>
