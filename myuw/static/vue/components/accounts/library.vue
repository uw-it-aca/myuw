<template>
  <uw-card :loaded="isReady"
           :errored="isErrored"
           :errored-show="showError"
  >
    <template #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Library Account
      </h3>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your library
      account information right now. In the meantime, try the
      <a href="http://www.lib.washington.edu/"
         data-linklabel="UW Libraries"
         target="_blank"
      >UW Libraries page</a>.
    </template>
    <template #card-body>
      <b-alert v-if="holdsReady" show variant="info">
        <font-awesome-icon :icon="['fas', 'info-circle']" />
        <a href="https://search.lib.uw.edu/account"
           target="_blank"
           data-linklabel="Library Account Requests"
           :v-text="itemsRequested"
        ></a>
      </b-alert>
      <div>
        <h4>
          Items out
        </h4>
        <span>
          {{ itemsLoaned + (isPlural(itemsLoaned) ? ' item' : ' items')}}
        </span>
      </div>

      <div v-if="nextDue">
        <h4>
          Next item due
        </h4>
        <span>

        </span>
      </div>

      <div>
        <a href="http://search.lib.uw.edu/account"
           target="_blank"
           aria-label="Your Library Account"
        >
          Access library account
        </a>
      </div>

    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import dayjs from 'dayjs';
import Card from '../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  data: function() {
    return {
      passwordChange: '',
    };
  },
  computed: {
    ...mapState({
      holdsReady: (state) => state.library.value.holds_ready,
      fines: (state) => state.library.value.fines,
      itemsLoaned: (state) => state.library.value.items_loaned,
      nextDue: (state) => state.library.value.next_due,
    }),
    ...mapGetters('library', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    showError() {
      return this.statusCode !== 404;
    },
    itemsRequestedText() {
      return this.holdsReady + ' requested ' +
             (isPlural(this.holdsReady) ? ' item ' : ' items ') + ' ready';
    },
  },
  mounted() {
    this.fetch();
  },
  methods: {
    toFriendlyDate(dateStr) {
      if (dateStr === undefined || dateStr.length === 0) {
        return '';
      }
      return dayjs(dateStr).format('ddd, MMM D');
    },
    isPlural(count) {
      return count !== 1;
    },
    ...mapActions('library', {
      fetch: 'fetch',
    }),
  },
};
</script>
