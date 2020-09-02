<template>
  <div v-if="estRegDate">
    <span class="sr-only">
      Estimated Registration Date: {{estRegDate.date}}
    </span>
    <h4>Est. Registration Date</h4>
    <div>
      <span>
        {{estRegDate.date}}
      </span>
      <br />
      <span>
        at 6:00 AM
      </span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    estRegDateNotices: {
      type: Array,
      required: true,
    },
    quarter: {
      type: String,
      required: true,
    }
  },
  data: function() {
    return {
      hasEstRegDataNotice: false,
      noticeMyRegIsOpen: false,
      isMy1stRegDay: false,
      estRegDate: null,
    }
  },
  created() {
    // Get estimated registration date for the quarter
    this.estRegDateNotices.forEach((notice) => {
      let registration_date = null;

      // Set registration_date date to the first date value found in
      // the notice attributes
      notice.attributes.filter((a) => a.name === 'Date')
        .slice(0, 1).forEach((a) => {registration_date = a.value});

      notice.attributes
        .filter((a) => a.name === 'Quarter' && a.value === this.quarter)
        .slice(0, 1).forEach((a) => {
          this.hasEstRegDataNotice = true;
          this.noticeMyRegIsOpen = notice.my_reg_has_opened;
          this.isMy1stRegDay = notice.is_my_1st_reg_day;
          this.estRegDate = {
            notice: notice,
            date: registration_date,
          };
        });
    });
  },
}
</script>

<style lang="scss" scoped>

</style>