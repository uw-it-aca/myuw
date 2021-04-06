<template>
  <div id="classlist_photo_view"
       class=""
       aria-labelledby="photo-grid"
  >
    <h3 class="sr-only">
      Grid of Student Photos
    </h3>
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
        <div>{{ reg.first_name }} {{ reg.surname }}</div>
        <div style="overflow-wrap: break-word;">{{ reg.pronouns }}</div>
      </li>
    </ol>
  </div>
</template>
<script>
export default {
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
};
</script>
