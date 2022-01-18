<template>
  <div id="classlist_photo_view"
       class=""
       aria-labelledby="photo-grid"
  >
    <h3 class="visually-hidden">
      Grid of Student Photos
    </h3>
    <ol class="list-unstyled d-flex flex-wrap">
      <li v-for="(reg, i) in registrations"
          :id="`student-photo-${reg.regid}`"
          :key="i"
          class="p-1 mb-1"
          :class="reg.isJoint ? (showJointCourseStud ? 'd-inline' : 'd-none') : 'd-inline'"
      >
        <div style="width: 120px">
          <img :src=" '/photo/' + reg.url_key"
              class=""
              width="120px" height="150px"
          >
          <strong>{{ reg.first_name }} {{ reg.surname }}</strong>
          <!-- <div class="myuw-text-sm">{{ reg.pronouns }}</div> -->
        </div>
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
