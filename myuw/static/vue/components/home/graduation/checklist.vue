<template>
  <uw-card v-if="true" :loaded="true">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Graduation: Checklist</h2>
    </template>
    <template #card-body>
      <div class="row">
        <div class="col-8">
          <p>
            <strong>To graduate, you'll need apply.</strong> Dont worry, it's an easy process you
            complete with your departmental adviser!
          </p>
        </div>
        <div class="col-4">One of three columns</div>
      </div>
    </template>
  </uw-card>
</template>

<script>

import Card from '../../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  computed: {},
};
</script>

<style lang="scss" scoped></style>
