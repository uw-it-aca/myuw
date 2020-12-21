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
          :class="reg.isJoint ? (showJointCourseStud ? 'd-inline' : 'd-none') : 'd-inline'"
      >
        <img :src=" '/photo/' + reg.url_key"
             class=""
             width="120px" height="150px"
        >
        {{ reg.first_name }} {{ reg.surname }}
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
  }
};
</script>
