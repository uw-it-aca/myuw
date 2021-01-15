<template>
  <div>
    <uw-section
      v-for="section in sections"
      :key="section.id"
      :section="section"
    >
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
    sections: {
      type: Array,
      required: true,
    },
  },
};
</script>
