<template>
  <span v-if="showCard">
    <font-awesome-icon :icon="faSyringe" />
    You are currently registered as NOT vaccinated.
  </span>
</template>

<script>
import {
  faSyringe,
} from '@fortawesome/free-solid-svg-icons';
import {mapGetters, mapState, mapActions} from 'vuex';

export default {
  data: function() {
    return {
      faSyringe,
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
