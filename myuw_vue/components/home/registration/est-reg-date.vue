<template>
  <div v-if="estRegData.estRegDate" class="mb-4">
    <div
      v-if="estRegData.isMy1stRegDay"
      class="alert alert-primary myuw-text-md"
      role="alert"
    >
      Registration opens at 6:00AM
    </div>

    <uw-card-status v-else>
      <template #status-label>Est. Registration Date</template>
      <template #status-value>
        <uw-formatted-date :due-date="estRegData.estRegDate" />
      </template>
      <template #status-content>
        <div class="d-flex myuw-text-md">
          <div class="flex-fill w-50"></div>
          <div class="flex-fill w-50 text-end">at 6:00 AM</div>
        </div>
      </template>
    </uw-card-status>
  </div>
</template>

<script>
import CardStatus from '../../_templates/card-status.vue';
import FormattedDate from '../../_common/formatted-date.vue';
export default {
  components: {
    'uw-card-status': CardStatus,
    'uw-formatted-date': FormattedDate,
  },
  props: {
    estRegData: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>

</style>
