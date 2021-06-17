<template>
  <p v-if="showCard">You are currently registered as NOT vaccinated. You should get vaccinated!</p>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';

export default {
  data() {
    return {
    };
  },
  computed: {
    ...mapState({
      student: (state) => state.user.affiliations.student,
    }),
    ...mapState('covid19', {
      covid19: (state) => state.value,
    }),
    ...mapGetters('covid19', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    showCard() {
      return this.student && this.statusCode === 404;
    }
  },
  mounted() {
    this.fetch();
  },
  methods: {
    ...mapActions('covid19', ['fetch']),
  },
};
</script>
