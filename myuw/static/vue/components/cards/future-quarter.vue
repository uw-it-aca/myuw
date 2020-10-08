<template>
  <div v-if="student">
    <div v-if="isReady">
      <div v-if="terms.length && shouldRender">
        <h3 class="sr-only">
          Upcoming quarters you are registered for
        </h3>
        <div v-for="(term, i) in terms" :key="i" >
          <uw-card v-if="term.has_registration" loaded>
            <template #card-heading>
              <h4 class="h3 text-dark-beige">
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
                <div class="position-absolute myuw-future-quarter">
                  <a :href="`../future_quarters${term.url}`"
                    class="d-inline-block text-center"
                  >
                    <span class="sr-only">
                      View {{ term.quarter }} {{ term.year }}
                      <span v-if="term.summer_term" class="text-capitalize">
                        {{ term.summer_term }}
                      </span>
                      information
                    </span>
                    <font-awesome-icon :icon="['fa', 'chevron-right']" class="" />
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
        <h3 class="text-dark-beige">
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

<style lang="scss" scoped>
@import "../../../css/myuw/variables.scss";
.myuw-future-quarter {
  right: 1rem; top: 50%; margin-top: -20px;
  a {
    line-height:40px; width: 40px;
    &:focus, &:focus-within, &:hover {
      background-color: $gray-200;
    }
  }
}
</style>
