<template>
  <div id="classlist_photo_view"
       class=""
       aria-labelledby="grid_view"
       role="tabpanel"
       aria-hidden="true" hidden="true"
  >
    <h4 class="sr-only">
      Grid of Student Photos
    </h4>
    <ol class="">
      <li v-for="(reg, i) in registrations"
          id="`student-photo-${reg.regid}`"
          :key="i"
          class="getClass(reg)"
      >
        <div class="">
          <img src="`/photo/${reg.url_key}`"
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
  },
  methods: {
    getClass(reg) {
      return reg.is_joint ? 'joint' : '';
    },
  },
};
</script>
