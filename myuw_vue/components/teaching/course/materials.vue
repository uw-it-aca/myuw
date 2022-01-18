<template>
  <uw-card-property-group>
    <uw-card-property title="Course Materials">
      <a v-if="section.myuwclass_url" :href="section.myuwclass_url">
        <img :src="`${staticUrl}images/myuwclasslink.gif`" width="67px" height="24px" />
      </a>
      <ul class="mb-0 list-unstyled">
        <li class="mb-1"><uw-teach-website :section="section" /></li>
        <li class="mb-1"><uw-teach-email-list :section="section" /></li>
        <li class="mb-1"><uw-teach-canvas :section="section" /></li>
        <li class="mb-1"><uw-teach-textbook v-if="!section.mini_card" :section="section" /></li>
      </ul>
    </uw-card-property>
  </uw-card-property-group>
</template>

<script>
import { mapState } from 'vuex';
import Canvas from './materials/canvas.vue';
import Website from './materials/website.vue';
import EmailList from './materials/email-list.vue';
import Textbook from './materials/textbook.vue';
import CardPropertyGroup from '../../_templates/card-property-group.vue';
import CardProperty from '../../_templates/card-property.vue';

export default {
  components: {
    'uw-card-property-group': CardPropertyGroup,
    'uw-card-property': CardProperty,
    'uw-teach-canvas': Canvas,
    'uw-teach-website': Website,
    'uw-teach-email-list': EmailList,
    'uw-teach-textbook': Textbook,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
  computed: {
    ...mapState({
      staticUrl: (state) => state.staticUrl,
    }),
  },
};
</script>
