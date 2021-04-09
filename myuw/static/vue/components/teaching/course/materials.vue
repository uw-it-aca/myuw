<template>
  <div>
    <h3 class="h6 text-dark-beige myuw-font-encode-sans"
      :class="{'sr-only': showRowHeader}">
      Course Materials
    </h3>
    <ul>
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
