<template>
  <div :class="dueIn30Days ? 'text-danger' : ''">
    {{ formattedDate }}
  </div>
</template>

<script>
export default {
  props: {
    dueDate: {
      type: String,
      required: true,
    },
  },
  computed: {
    daysDiff() {
      return this.diffDays(this.dueDate);
    },
    dueIn30Days() {
      return this.daysDiff >= 0 && this.daysDiff <= 30;
    },
    dueIn3Days() {
      return this.daysDiff >= 0 && this.daysDiff <= 3;
    },
    formattedDate() {
      return (this.dueIn3Days
        ? this.toFriendlyDatetime(this.dueDate)
        : this.toFriendlyDate(this.dueDate));
    },
  }
};
</script>

<style lang="scss" scoped>
</style>
