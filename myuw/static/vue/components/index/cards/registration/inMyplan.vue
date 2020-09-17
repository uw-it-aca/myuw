<template>
  <div>myplan</div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';

export default {
  props: {
    nextTermYear: {
      type: Number,
      required: true,
    },
    nextTermQuarter: {
      type: String,
      required: true,
    }
  },
  computed: {
    ...mapState('myplan', {
    }),
    ...mapGetters('myplan', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
  },
  created() {
    this.fetchMyPlan(this.nextTermYear, this.nextTermQuarter);
  },
  methods: {
    ...mapActions('myplan', {
      fetchMyPlan: 'fetch',
    }),
  },
}
</script>

<style lang="scss" scoped>

</style>