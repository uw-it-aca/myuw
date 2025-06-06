<template>
  <div>
    <h3 class="h6 text-dark-beige myuw-font-encode-sans">ISS Portal</h3>
    <p class="myuw-text-md">
      Use the ISS Portal to check in with UWB's International Student Services
      and make requests for your immigration status.
      <br>
      <uw-link-button class="mt-2 mb-1" href="https://iss.uwb.edu">
        Go to ISS Portal
      </uw-link-button>
    </p>
    <h3 class="h6 text-dark-beige myuw-font-encode-sans">General information</h3>
    <p class="myuw-text-md">
        Use <a href="https://www.uwb.edu/international-student-services/"
        >the ISS website</a> to learn about your F-1 status and the benefits you can request.
    </p>
  </div>
</template>

<script>
import LinkButton from '../../_templates/link-button.vue';

export default {
  components: {
    'uw-link-button': LinkButton,
  },
};
</script>
