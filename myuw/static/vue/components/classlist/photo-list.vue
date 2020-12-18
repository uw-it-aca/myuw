<template>
  <div id="classlist_photo_view"
       class=""
       aria-labelledby="photo-grid"
  >
    <h4 class="sr-only">
      Grid of Student Photos
    </h4>
    <ol class="">
      <li v-for="(reg, i) in registrations"
          :id="`student-photo-${reg.regid}`"
          :key="i"
          :style="getClass(reg)"
      >
        <div class="">
          <img :src="getImgUrl(reg)"
               class=""
               width="120px" height="150px"
          >
        </div>
        <div class="">
          {{ reg.first_name }} {{ reg.surname }}
        </div>
      </li>
    </ol>
  </div>
</template>
<script>
export default {
  props: {
    mobileOnly: {
      type: Boolean,
      default: false,
    },
    registrations: {
      type: Array,
      required: true,
    },
    showJointCourseStud: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    getClass(reg) {
      if (reg.isJoint) {
        return this.showJointCourseStud ? 'display: inline' : 'display: none';
      }
      return 'display: inline';
    },
    getImgUrl(reg) {
      return '/photo/' + reg.url_key;
    },
  },
};
</script>
