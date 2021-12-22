<template>
  <uw-card v-if="true" :loaded="true">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Graduation: Checklist</h2>
    </template>
    <template #card-body>
      <p>
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Debitis dolorem labore a sit
        placeat nisi iusto ullam, ipsam vitae numquam ad, magni at ex quas ut magnam dignissimos
        incidunt nostrum.
      </p>
    </template>
  </uw-card>
</template>

<script>
import Card from '../../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  computed: {

  },
};
</script>

<style lang="scss" scoped></style>
