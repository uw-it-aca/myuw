<template>
  <uw-card loaded>
    <template #card-heading>
      No {{ ucfirst(quarter) }} {{ ucfirst(summerTerm) }} Registration Found
    </template>
    <template #card-body>
      <p>
        You don’t appear to be registered for any credit courses in
        {{ quarter }} {{ summerTerm }} quarter. If you think this is an
        error, please contact the
        <a href="https://itconnect.uw.edu/it-connect-home/question/"
           title="Send email to UW-IT Service Center"
        >
          UW-IT Service Center
        </a>.
      </p>

      <p>
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
