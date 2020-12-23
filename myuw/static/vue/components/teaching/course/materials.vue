<template>
  <div>
    <h5 :class="{'sr-only': showRowHeader}">
      Course Materials
    </h5>
    <ul>
      <uw-website :section="section" />
      <uw-email-list :section="section" />
    </ul>
  </div>
</template>

<script>
import Website from './materials/website.vue';
import EmailList from './materials/email-list.vue';

export default {
  components: {
    'uw-website': Website,
    'uw-email-list': EmailList,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
    showRowHeader: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
