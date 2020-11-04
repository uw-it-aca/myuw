<template>
  <uw-card loaded>
    <template #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        No {{ ucfirst(quarter) }} {{ ucfirst(summerTerm) }} Registration Found
      </h3>
    </template>
    <template #card-body>
      <p class="myuw-text-md">
        You don’t appear to be registered for any credit courses in
        {{ quarter }} {{ summerTerm }} quarter. If you think this is an
        error, please contact the
        <a href="https://itconnect.uw.edu/it-connect-home/question/"
           title="Send email to UW-IT Service Center"
        >
          UW-IT Service Center
        </a>.
      </p>

      <p class="mb-0 myuw-text-md">
        If you are interested in registration,
        <a href="../resource/academics">
          view registration resources.
        </a>
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
    quarter: {
      type: String,
      required: true,
      default: '',
    },
    summerTerm: {
      type: String,
      required: true,
      default: '',
    },
  },
};
</script>
