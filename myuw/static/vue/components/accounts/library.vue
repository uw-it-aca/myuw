<template>
  <uw-card :loaded="isReady" :errored="isErrored" :errored-show="showError">
    <template #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Library Account</h3>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your library account information right now. In the
      meantime, try the
      <a href="http://www.lib.washington.edu/" data-linklabel="UW Libraries" target="_blank"
        >UW Libraries page</a
      >.
    </template>
    <template #card-body>
      <b-alert v-if="holdsReady" show variant="info">
        <div class="d-flex text-default m-0 myuw-text-md">
          <div class="pr-2 flex-shrink-1">
            <font-awesome-icon :icon="faQuestionCircle" />
          </div>
          <div class="w-100">
            <a
              href="https://search.lib.uw.edu/account"
              target="_blank"
              data-linklabel="Library Account Requests"
              >{{ itemsRequestedText }}</a
            >
          </div>
        </div>
      </b-alert>

      <ul class="list-unstyled">
        <li>
          <uw-card-status>
            <template #status-label>Items out</template>
            <template #status-value>
              {{ itemsLoaned + (isPlural(itemsLoaned) ? ' items' : ' item') }}
            </template>
          </uw-card-status>
        </li>
        <li v-if="nextDue">
          <uw-card-status>
            <template #status-label>Next item due</template>
            <template #status-value>
              {{ toFromNowDate(nextDue) }}
            </template>
            <template #status-content>
              <div class="myuw-text-sm text-muted text-right">
                {{ toFriendlyDatetime(nextDue) }}
              </div>
            </template>
          </uw-card-status>
        </li>
        <li v-if="fines">
          <uw-card-status>
            <template #status-label>You owe</template>
            <template #status-value>
              <span class="text-danger">
                {{ formatPrice(fines) }}
              </span>
            </template>
            <template #status-content>
              <div class="myuw-text-sm text-muted text-right">
                <a
                  href="https://p.lib.washington.edu/payfines/"
                  target="_blank"
                  data-linklabel="Pay Library Fees"
                >
                  Pay fees
                </a>
              </div>
            </template>
          </uw-card-status>
        </li>
      </ul>

      <div class="text-right">
        <uw-link-button href="http://search.lib.uw.edu/account" target="_blank">
          Access library account
        </uw-link-button>
      </div>
    </template>
  </uw-card>
</template>

<script>
import {
  faQuestionCircle,
} from '@fortawesome/free-solid-svg-icons';
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../_templates/card.vue';
import CardStatus from '../_templates/card-status.vue';
import LinkButton from '../_templates/link-button.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-card-status': CardStatus,
    'uw-link-button': LinkButton,
  },
  data() {
    return {
      faQuestionCircle,
    }
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
      return (
        this.holdsReady +
        ' requested ' +
        (this.isPlural(this.holdsReady) ? 'items ' : 'item ') +
        'ready'
      );
    },
  },
  mounted() {
    this.fetch();
  },
  methods: {
    isPlural(count) {
      return count !== 1;
    },
    ...mapActions('library', {
      fetch: 'fetch',
    }),
  },
};
</script>
