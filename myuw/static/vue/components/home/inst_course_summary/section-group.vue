<template>
  <div>
    <uw-section :section="section">
      <slot />
    </uw-section>
  </div>
</template>

<script>
import Section from './section.vue';

export default {
  components: {
    'uw-section': Section,
  },
  props: {
    mobileOnly: {
      type: Boolean,
      default: false,
    },
    section: {
      type: Object,
      required: true,
    },
  },
};
</script>
