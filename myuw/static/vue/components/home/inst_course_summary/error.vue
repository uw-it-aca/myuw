<template>
  <uw-card v-if="statusCode !== 404">
    <template #card-heading>
      <h3>
        {{ ucfirst(quarter) }} {{ year }} Teaching Schedule
      </h3>
    </template>
    <template #card-body>
      <p v-if="statusCode === 410">
        The page you seek is for a past quarter and is no longer available.
      </p>
      <p v-else>
        <i class="fa fa-exclamation-triangle" />
        An error occurred and MyUW cannot load your teaching schedule
        right now. In the meantime, try the
        <a
          href="https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/default.aspx"
          data-linklabel="MyClass" target="_blank"
        >
          My Class Instructor Resources
        </a> page.
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
  props: {
    statusCode: {
      type: Number,
      required: true,
    },
    year: {
      type: String,
      required: true,
    },
    quarter: {
      type: String,
      required: true,
    },
  },
};
</script>
