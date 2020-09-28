<template>
  <div v-if="student">
    <div v-if="isReady">
      <div v-if="terms.length && shouldRender">
        <h3>Upcoming quarters you are registered for</h3>
        <uw-card
          v-for="(term, i) in terms"
          :key="i" :loaded="true"
        >
          <template #card-heading>
            <h4>
              {{ term.quarter }} {{ term.year }}
              <span v-if="term.summer_term" class="text-capitalize">
                {{ term.summer_term }}
              </span>
            </h4>
          </template>
          <template #card-body>
            <p>
              <span>
                You have registered for {{ term.credits }} credits
              </span>
              <span>
                ({{ term.section_count }}
                {{ term.section_count > 1 ? "sections" : "section" }})
                for {{ term.quarter }} {{ term.year }}
                <span v-if="term.summer_term" class="text-capitalize">
                  {{ term.summer_term }}
                </span>
              </span>
            </p>
            <div>
              <a :href="`../future_quarters${term.url}`">
                <span>
                  View {{ term.quarter }} {{ term.year }}
                  <span v-if="term.summer_term" class="text-capitalize">
                    {{ term.summer_term }}
                  </span>
                  information
                </span>
                <font-awesome-icon :icon="['fa', 'chevron-right']" />
              </a>
            </div>
          </template>
        </uw-card>
      </div>
    </div>
    <uw-card
      v-else
      :loaded="false"
      :errored="isErrored"
      :errored-show="showError"
    />
  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../containers/card.vue';

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
      return this.statusCode === 543;
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
