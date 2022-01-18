<template>
  <div class="card-property-group">
    <slot />
    <uw-card-property title="" class="card-group-divider">
      <hr class="my-1 bg-secondary">
    </uw-card-property>
  </div>
</template>

<script>
import CardProperty from './card-property.vue';

export default {
  components: {
    'uw-card-property': CardProperty,
  },
  data() {
    return {};
  },
};
</script>
