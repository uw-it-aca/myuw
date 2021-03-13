<template>
  <div v-if="student">
    <div v-if="isReady">
      <div v-if="terms.length && shouldRender">
        <h3 class="sr-only">
          Upcoming quarters you are registered for
        </h3>
        <div v-for="(term, i) in terms" :key="i">
          <uw-card v-if="term.has_registration" loaded>
            <template #card-heading>
              <h4 class="mb-3 text-dark-beige myuw-font-encode-sans">
                {{ term.quarter }} {{ term.year }}
                <span v-if="term.summer_term" class="text-capitalize">
                  {{ term.summer_term }}
                </span>
              </h4>
            </template>
            <template #card-body>
              <div>
                <div class="myuw-text-md mr-auto">
                  <div>
                    You have registered for {{ term.credits }} credits
                  </div>
                  <div>
                    ({{ term.section_count }}
                    {{ term.section_count > 1 ? "sections" : "section" }})
                    for {{ term.quarter }} {{ term.year }}
                    <span v-if="term.summer_term" class="text-capitalize">
                      {{ term.summer_term }}
                    </span>
                  </div>
                </div>
                <div class="myuw-chevron">
                  <a
                    v-out="'View future quarter courses'"
                    :href="`../future_quarters${term.url}`">
                    <span class="sr-only">
                      View {{ term.quarter }} {{ term.year }}
                      <span v-if="term.summer_term" class="text-capitalize">
                        {{ term.summer_term }}
                      </span>
                      information
                    </span>
                    <font-awesome-icon
                      :icon="['fa', 'chevron-right']"
                    />
                  </a>
                </div>
              </div>
            </template>
          </uw-card>
        </div>
      </div>
    </div>
    <uw-card
      v-else-if="highlighted"
      :loaded="false"
      :errored="isErrored"
      :errored-show="showError"
    >
      <template #card-heading>
        <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
          Future Quarter
        </h3>
      </template>
      <template #card-error>
        An error occurred and MyUW cannot load your registration information
        right now. Please try again later.
      </template>
    </uw-card>
  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  props: {
    highlighted: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapState({
      student: (state) => state.user.affiliations.student,
    }),
    ...mapState('oquarter', {
      terms: (state) => state.value.terms,
      highlightFutureQuarters: (state) => state.value.highlight_future_quarters,
    }),
    ...mapGetters('oquarter', [
      'isReady',
      'isErrored',
      'statusCode',
    ]),
    shouldRender() {
      return (
        this.highlightFutureQuarters && this.highlighted
      ) || !this.highlighted && !this.highlightFutureQuarters;
    },
    showError: function() {
      return this.statusCode !== 404;
    },
  },
  created() {
    this.fetch();
  },
  methods: {
    ...mapActions('oquarter', ['fetch']),
  },
};
</script>
