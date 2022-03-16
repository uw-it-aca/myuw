<template>
  <div :class="displayTextDanger && dueIn30Days ? 'text-danger' : ''">
    {{ formattedDate }}
  </div>
</template>

<script>
export default {
  props: {
    dueDate: {  // a timezone aware datetime string
      type: String,
      required: true,
    },
    displayTextDanger: {
      type: Boolean,
      default: false,
    },
    displayTime: {
      type: Boolean,
      default: false,
    }
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
      return (this.displayTime && this.dueIn3Days
        ? this.toFriendlyDatetime(this.dueDate)
        : this.toFriendlyDate(this.dueDate));
    },
  }
};
</script>

<style lang="scss" scoped>
</style>
