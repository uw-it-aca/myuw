<template>
  <div>
    <h5 :class="{'sr-only': showRowHeader}">
      Course Materials
    </h5>
    <ul>
      <uw-website :section="section" />
      <uw-email-list :section="section" />
      <uw-canvas :section="section" />
      <uw-textbook v-if="!section.mini_card" :section="section" />
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
    'uw-canvas': Canvas,
    'uw-website': Website,
    'uw-email-list': EmailList,
    'uw-textbook': Textbook,
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
