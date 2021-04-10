<template>
  <div class="d-flex">
    <h3 class="w-25 myuw-text-md myuw-font-encode-sans"
      :class="{'sr-only': showRowHeader}">
      Course Materials
    </h3>
    <ul class="w-75">
      <uw-teac-website :section="section" />
      <uw-teac-email-list :section="section" />
      <uw-teac-canvas :section="section" />
      <uw-teac-textbook v-if="!section.mini_card" :section="section" />
    </ul>
  </div>
</template>

<script>
import Canvas from './materials/canvas.vue';
import Website from './materials/website.vue';
import EmailList from './materials/email-list.vue';
import Textbook from './materials/textbook.vue';

export default {
  components: {
    'uw-teac-canvas': Canvas,
    'uw-teac-website': Website,
    'uw-teac-email-list': EmailList,
    'uw-teac-textbook': Textbook,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
    showRowHeader: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
